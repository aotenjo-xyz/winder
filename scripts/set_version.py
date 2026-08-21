#!/usr/bin/env python3
"""Synchronize the Winder version across Python, npm, Cargo, and Tauri metadata."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
VERSION_PATTERN = re.compile(
    r"^v?(?P<major>0|[1-9]\d*)\."
    r"(?P<minor>0|[1-9]\d*)\."
    r"(?P<patch>0|[1-9]\d*)"
    r"(?:-(?P<stage>alpha|beta|rc)\.(?P<number>0|[1-9]\d*))?$"
)


def parse_version(raw_version: str) -> tuple[str, str]:
    match = VERSION_PATTERN.fullmatch(raw_version)
    if match is None:
        raise ValueError(
            "Version must look like 1.2.3, 1.2.3-alpha.1, "
            "1.2.3-beta.1, or 1.2.3-rc.1"
        )

    base = ".".join(match.group(name) for name in ("major", "minor", "patch"))
    stage = match.group("stage")
    number = match.group("number")
    if stage is None:
        return base, base

    app_version = f"{base}-{stage}.{number}"
    pep440_stage = {"alpha": "a", "beta": "b", "rc": "rc"}[stage]
    python_version = f"{base}{pep440_stage}{number}"
    return app_version, python_version


def replace_section_version(text: str, section: str, version: str) -> str:
    pattern = re.compile(
        rf"(^\[{re.escape(section)}\]\s*$(?P<body>.*?))(?=^\[|\Z)",
        re.MULTILINE | re.DOTALL,
    )
    match = pattern.search(text)
    if match is None:
        raise ValueError(f"Missing [{section}] section")

    block = match.group(0)
    updated, count = re.subn(
        r'(?m)^version\s*=\s*"[^"]+"', f'version = "{version}"', block, count=1
    )
    if count != 1:
        raise ValueError(f"Missing version in [{section}] section")
    return text[: match.start()] + updated + text[match.end() :]


def replace_locked_package_version(text: str, package: str, version: str) -> str:
    pattern = re.compile(
        rf'(^\[\[package\]\]\s*$\s*^name\s*=\s*"{re.escape(package)}"\s*$)'
        rf"(?P<body>.*?)(?=^\[\[package\]\]|\Z)",
        re.MULTILINE | re.DOTALL,
    )
    match = pattern.search(text)
    if match is None:
        raise ValueError(f'Missing package "{package}" in lock file')

    block = match.group(0)
    updated, count = re.subn(
        r'(?m)^version\s*=\s*"[^"]+"', f'version = "{version}"', block, count=1
    )
    if count != 1:
        raise ValueError(f'Missing version for package "{package}"')
    return text[: match.start()] + updated + text[match.end() :]


def json_text(data: object) -> str:
    return json.dumps(data, indent=2, ensure_ascii=False) + "\n"


def build_updates(app_version: str, python_version: str) -> dict[Path, str]:
    pyproject = REPO_ROOT / "pyproject.toml"
    cargo_toml = REPO_ROOT / "gui/frontend/src-tauri/Cargo.toml"
    cargo_lock = REPO_ROOT / "gui/frontend/src-tauri/Cargo.lock"
    tauri_config = REPO_ROOT / "gui/frontend/src-tauri/tauri.conf.json"
    package_json = REPO_ROOT / "gui/frontend/package.json"
    package_lock = REPO_ROOT / "gui/frontend/package-lock.json"
    uv_lock = REPO_ROOT / "uv.lock"

    package_data = json.loads(package_json.read_text(encoding="utf-8"))
    package_data["version"] = app_version

    package_lock_data = json.loads(package_lock.read_text(encoding="utf-8"))
    package_lock_data["version"] = app_version
    package_lock_data["packages"][""]["version"] = app_version

    tauri_data = json.loads(tauri_config.read_text(encoding="utf-8"))
    tauri_data["version"] = app_version

    return {
        pyproject: replace_section_version(
            pyproject.read_text(encoding="utf-8"), "project", python_version
        ),
        uv_lock: replace_locked_package_version(
            uv_lock.read_text(encoding="utf-8"), "winder", python_version
        ),
        package_json: json_text(package_data),
        package_lock: json_text(package_lock_data),
        cargo_toml: replace_section_version(
            cargo_toml.read_text(encoding="utf-8"), "package", app_version
        ),
        cargo_lock: replace_locked_package_version(
            cargo_lock.read_text(encoding="utf-8"), "winder-gui", app_version
        ),
        tauri_config: json_text(tauri_data),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("version", help="New version, optionally prefixed with v")
    parser.add_argument(
        "--dry-run", action="store_true", help="Validate and show affected files only"
    )
    args = parser.parse_args()

    try:
        app_version, python_version = parse_version(args.version)
        updates = build_updates(app_version, python_version)
    except (KeyError, OSError, ValueError, json.JSONDecodeError) as exc:
        parser.error(str(exc))

    changed = [path for path, content in updates.items() if path.read_text() != content]
    action = "Would update" if args.dry_run else "Updated"
    if not args.dry_run:
        for path in changed:
            path.write_text(updates[path], encoding="utf-8")

    print(f"Application version: {app_version}")
    print(f"Python version:      {python_version}")
    if changed:
        for path in changed:
            print(f"{action}: {path.relative_to(REPO_ROOT)}")
    else:
        print("All version fields are already synchronized.")


if __name__ == "__main__":
    main()
