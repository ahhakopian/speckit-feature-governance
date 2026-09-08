#!/usr/bin/env python3
"""Global bootstrap/sync shim for Spec Kit Feature Governance.

This script deliberately does not change global Codex instructions. It only
installs/synchronizes the governance preset and extension into Spec Kit
projects, and the resulting Spec Kit command wrappers load one global policy.

Default global home:
    ~/.config/speckit-feature-governance

Environment variables:
    SPECKIT_FEATURE_GOVERNANCE_HOME
        Override the global governance home.

    SPECKIT_FEATURE_GOVERNANCE_AUTO_UPDATE
        "1" (default) performs a best-effort `git pull --ff-only` when the
        global home itself is a Git checkout. Set to "0" to disable.

    SPECKIT_UPSTREAM_SPECIFY
        Path/name of the real upstream `specify` executable. Default: specify.

Exit code 75 from `ensure-project` means project command/skill materialization
was refreshed and the current Spec Kit command should be invoked again so the
agent reloads the new command content.
"""

from __future__ import annotations

import argparse
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Iterable

GOVERNANCE_HOME_DEFAULT = Path.home() / ".config" / "speckit-feature-governance"
PRESET_ID = "feature-governance"
EXTENSION_ID = "feature-governance-guard"
RESTART_REQUIRED = 75

REQUIRED_RELATIVE_FILES = (
    Path("preset/preset.yml"),
    Path("preset/commands/speckit.specify.md"),
    Path("preset/commands/speckit.plan.md"),
    Path("preset/commands/speckit.tasks.md"),
    Path("preset/commands/speckit.analyze.md"),
    Path("extension/extension.yml"),
    Path("extension/commands/speckit.feature-governance.review.md"),
    Path("extension/docs/feature-architecture-policy.md"),
    Path("bootstrap/specify-governed.py"),
)


def eprint(*args: object) -> None:
    print(*args, file=sys.stderr)


def governance_home() -> Path:
    raw = os.environ.get("SPECKIT_FEATURE_GOVERNANCE_HOME")
    return Path(raw).expanduser().resolve() if raw else GOVERNANCE_HOME_DEFAULT.resolve()


def upstream_specify() -> str:
    return os.environ.get("SPECKIT_UPSTREAM_SPECIFY", "specify")


def run(cmd: list[str], cwd: Path | None = None, quiet: bool = False, check: bool = True) -> subprocess.CompletedProcess[str]:
    if not quiet:
        print("+", " ".join(cmd))
    return subprocess.run(
        cmd,
        cwd=str(cwd) if cwd else None,
        text=True,
        stdout=subprocess.PIPE if quiet else None,
        stderr=subprocess.PIPE if quiet else None,
        check=check,
    )


def validate_source(root: Path) -> list[str]:
    errors: list[str] = []
    for rel in REQUIRED_RELATIVE_FILES:
        if not (root / rel).is_file():
            errors.append(f"missing required file: {rel}")

    preset = root / "preset/preset.yml"
    extension = root / "extension/extension.yml"
    if preset.is_file() and manifest_version(preset) is None:
        errors.append("could not read preset version")
    if extension.is_file() and manifest_version(extension) is None:
        errors.append("could not read extension version")
    return errors


def manifest_version(path: Path) -> str | None:
    """Extract the first semantic version field without requiring PyYAML."""
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return None
    match = re.search(r'^\s*version:\s*["\']?([0-9]+\.[0-9]+\.[0-9]+)["\']?\s*$', text, re.MULTILINE)
    return match.group(1) if match else None


def copy_tree_contents(source: Path, destination: Path) -> None:
    destination.mkdir(parents=True, exist_ok=True)
    for item in source.iterdir():
        if item.name == ".git":
            continue
        target = destination / item.name
        if item.is_dir():
            if target.exists():
                shutil.rmtree(target)
            shutil.copytree(item, target)
        else:
            shutil.copy2(item, target)


def best_effort_global_update(home: Path, quiet: bool) -> None:
    if os.environ.get("SPECKIT_FEATURE_GOVERNANCE_AUTO_UPDATE", "1") == "0":
        return
    if not (home / ".git").is_dir() or shutil.which("git") is None:
        return
    try:
        result = run(["git", "pull", "--ff-only"], cwd=home, quiet=True, check=False)
        if result.returncode != 0 and not quiet:
            eprint("Warning: governance git update failed; using the last local version.")
            if result.stderr:
                eprint(result.stderr.strip())
    except OSError as exc:
        if not quiet:
            eprint(f"Warning: governance git update failed: {exc}")


def find_project_root(start: Path) -> Path | None:
    start = start.resolve()
    for candidate in (start, *start.parents):
        if (candidate / ".specify").is_dir():
            return candidate
    return None


def installed_version(project: Path, kind: str, ident: str, manifest: str) -> str | None:
    return manifest_version(project / ".specify" / kind / ident / manifest)


def ensure_component_versions(project: Path, home: Path, quiet: bool) -> bool:
    """Install/reinstall governance components when absent or version-mismatched.

    Returns True when agent command/skill materialization may have changed.
    """
    preset_src = home / "preset"
    extension_src = home / "extension"
    global_preset_version = manifest_version(preset_src / "preset.yml")
    global_extension_version = manifest_version(extension_src / "extension.yml")
    if not global_preset_version or not global_extension_version:
        raise RuntimeError("global governance manifests are invalid or missing versions")

    project_preset_version = installed_version(project, "presets", PRESET_ID, "preset.yml")
    project_extension_version = installed_version(project, "extensions", EXTENSION_ID, "extension.yml")
    changed = False
    specify = upstream_specify()

    # Extension first so its namespaced review command exists before hook use.
    if project_extension_version != global_extension_version:
        cmd = [specify, "extension", "add", "--dev", str(extension_src), "--force", "--priority", "5"]
        result = run(cmd, cwd=project, quiet=quiet, check=False)
        if result.returncode != 0:
            detail = (result.stderr or result.stdout or "").strip()
            raise RuntimeError(f"failed to install/update {EXTENSION_ID}: {detail}")
        changed = True

    if project_preset_version != global_preset_version:
        if project_preset_version is not None:
            result = run([specify, "preset", "remove", PRESET_ID], cwd=project, quiet=quiet, check=False)
            if result.returncode != 0:
                detail = (result.stderr or result.stdout or "").strip()
                raise RuntimeError(f"failed to remove old {PRESET_ID}: {detail}")
        result = run([specify, "preset", "add", "--dev", str(preset_src), "--priority", "5"], cwd=project, quiet=quiet, check=False)
        if result.returncode != 0:
            detail = (result.stderr or result.stdout or "").strip()
            raise RuntimeError(f"failed to install/update {PRESET_ID}: {detail}")
        changed = True

    return changed


def cmd_install_global(args: argparse.Namespace) -> int:
    home = governance_home()
    if args.repo:
        if home.exists() and any(home.iterdir()):
            if not args.force:
                eprint(f"Global governance home is not empty: {home}")
                eprint("Use --force to replace it, or update the existing checkout.")
                return 2
            shutil.rmtree(home)
        home.parent.mkdir(parents=True, exist_ok=True)
        result = run(["git", "clone", "--depth", "1", args.repo, str(home)], check=False)
        if result.returncode != 0:
            return result.returncode
    else:
        source = Path(args.source).expanduser().resolve() if args.source else Path(__file__).resolve().parents[1]
        errors = validate_source(source)
        if errors:
            for error in errors:
                eprint("Error:", error)
            return 2
        if source == home:
            print(f"Global governance already lives at {home}")
            return 0
        if home.exists() and args.force:
            shutil.rmtree(home)
        elif home.exists() and any(home.iterdir()):
            eprint(f"Global governance home is not empty: {home}")
            eprint("Use --force to replace it.")
            return 2
        copy_tree_contents(source, home)

    errors = validate_source(home)
    if errors:
        for error in errors:
            eprint("Error:", error)
        return 2
    print(f"Installed global Feature Governance at {home}")
    return 0


def cmd_ensure_project(args: argparse.Namespace) -> int:
    home = governance_home()
    errors = validate_source(home)
    if errors:
        if not args.quiet:
            for error in errors:
                eprint("Error:", error)
            eprint(f"Install governance first at {home} using the 'install-global' command.")
        return 2

    best_effort_global_update(home, args.quiet)
    # Revalidate in case an update changed the checkout.
    errors = validate_source(home)
    if errors:
        if not args.quiet:
            for error in errors:
                eprint("Error after global update:", error)
        return 2

    start = Path(args.project_root).expanduser() if args.project_root else Path.cwd()
    project = find_project_root(start)
    if project is None:
        if not args.quiet:
            eprint("Error: not inside a Spec Kit project (.specify not found).")
        return 2

    try:
        changed = ensure_component_versions(project, home, args.quiet)
    except (OSError, RuntimeError) as exc:
        if not args.quiet:
            eprint(f"Error: {exc}")
        return 2

    if changed:
        print("GOVERNANCE_UPDATED_RESTART_REQUIRED")
        return RESTART_REQUIRED
    if not args.quiet:
        print("Feature Governance is current.")
    return 0


def infer_init_project_root(init_args: list[str], cwd: Path) -> Path | None:
    if "--here" in init_args or "." in init_args:
        return cwd.resolve()

    # First non-option token after `init` is the project name. Skip values for
    # common options that take arguments.
    options_with_values = {
        "--integration", "--ai", "--script", "--preset", "--integration-options"
    }
    skip_next = False
    for token in init_args:
        if skip_next:
            skip_next = False
            continue
        if token in options_with_values:
            skip_next = True
            continue
        if token.startswith("--"):
            continue
        return (cwd / token).resolve()
    return None


def cmd_init(args: argparse.Namespace) -> int:
    home = governance_home()
    errors = validate_source(home)
    if errors:
        for error in errors:
            eprint("Error:", error)
        eprint("Run install-global first.")
        return 2
    best_effort_global_update(home, quiet=False)

    upstream_args = list(args.specify_args)
    if upstream_args and upstream_args[0] == "--":
        upstream_args = upstream_args[1:]
    result = run([upstream_specify(), "init", *upstream_args], cwd=Path.cwd(), check=False)
    if result.returncode != 0:
        return result.returncode

    project = infer_init_project_root(upstream_args, Path.cwd())
    if project is None or not (project / ".specify").is_dir():
        eprint("Spec Kit init succeeded, but project root could not be resolved automatically.")
        eprint("Run: specify-governed.py ensure-project --project-root <path>")
        return 2
    try:
        ensure_component_versions(project, home, quiet=False)
    except (OSError, RuntimeError) as exc:
        eprint(f"Error installing governance into initialized project: {exc}")
        return 2
    print(f"Initialized governed Spec Kit project: {project}")
    return 0


def cmd_doctor(args: argparse.Namespace) -> int:
    root = Path(args.source_root).expanduser().resolve() if args.source_root else governance_home()
    errors = validate_source(root)
    if errors:
        for error in errors:
            eprint("FAIL:", error)
        return 2
    print(f"OK: governance source is structurally valid: {root}")
    print(f"Preset version: {manifest_version(root / 'preset/preset.yml')}")
    print(f"Extension version: {manifest_version(root / 'extension/extension.yml')}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Global bootstrap/sync for Spec Kit Feature Governance")
    sub = parser.add_subparsers(dest="command", required=True)

    install = sub.add_parser("install-global", help="Install the governance package into the user-global home")
    source_group = install.add_mutually_exclusive_group()
    source_group.add_argument("--source", help="Local package root; defaults to this script's package root")
    source_group.add_argument("--repo", help="Git repository URL to clone into the global home")
    install.add_argument("--force", action="store_true", help="Replace an existing global home")
    install.set_defaults(func=cmd_install_global)

    ensure = sub.add_parser("ensure-project", help="Sync governance into an existing Spec Kit project")
    ensure.add_argument("--project-root", default=".", help="Project path or a path inside the project")
    ensure.add_argument("--quiet", action="store_true", help="Suppress normal status output")
    ensure.set_defaults(func=cmd_ensure_project)

    init = sub.add_parser("init", help="Run upstream `specify init`, then install governance")
    init.add_argument("specify_args", nargs=argparse.REMAINDER, help="Arguments passed to upstream `specify init`")
    init.set_defaults(func=cmd_init)

    doctor = sub.add_parser("doctor", help="Validate the global/source package structure")
    doctor.add_argument("--source-root", help="Validate this package root instead of the global home")
    doctor.set_defaults(func=cmd_doctor)

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    return int(args.func(args))


if __name__ == "__main__":
    raise SystemExit(main())
