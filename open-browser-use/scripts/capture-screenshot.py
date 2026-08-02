#!/usr/bin/env python3
"""Capture an Open Browser Use tab to a PNG file through CDP."""

from __future__ import annotations

import argparse
import base64
import binascii
import json
import os
from pathlib import Path
import subprocess
import sys
from typing import Any

PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--session-id", required=True)
    parser.add_argument("--tab-id", required=True, type=int)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--full-page", action="store_true")
    parser.add_argument("--browser")
    parser.add_argument("--profile")
    parser.add_argument("--socket")
    parser.add_argument("--force", action="store_true")
    return parser.parse_args()


def cdp(args: argparse.Namespace, method: str, params: dict[str, Any]) -> Any:
    command = [
        "open-browser-use",
        "cdp",
        "--session-id",
        args.session_id,
        "--tab-id",
        str(args.tab_id),
        "--method",
        method,
        "--params",
        json.dumps(params, separators=(",", ":")),
        "--timeout",
        "30s",
    ]
    for option in ("browser", "profile", "socket"):
        value = getattr(args, option)
        if value:
            command.extend((f"--{option}", value))

    result = subprocess.run(command, capture_output=True, text=True)
    if result.returncode:
        detail = result.stderr.strip() or result.stdout.strip()
        raise RuntimeError(f"{method} failed: {detail}")
    try:
        return json.loads(result.stdout)
    except json.JSONDecodeError as error:
        raise RuntimeError(f"{method} returned invalid JSON: {error}") from error


def find_mapping(value: Any, key: str) -> dict[str, Any] | None:
    if isinstance(value, dict):
        candidate = value.get(key)
        if isinstance(candidate, dict):
            return candidate
        for child in value.values():
            found = find_mapping(child, key)
            if found is not None:
                return found
    elif isinstance(value, list):
        for child in value:
            found = find_mapping(child, key)
            if found is not None:
                return found
    return None


def find_string(value: Any, key: str) -> str | None:
    if isinstance(value, dict):
        candidate = value.get(key)
        if isinstance(candidate, str):
            return candidate
        for child in value.values():
            found = find_string(child, key)
            if found is not None:
                return found
    elif isinstance(value, list):
        for child in value:
            found = find_string(child, key)
            if found is not None:
                return found
    return None


def capture_params(args: argparse.Namespace) -> dict[str, Any]:
    params: dict[str, Any] = {
        "format": "png",
        "fromSurface": True,
        "captureBeyondViewport": args.full_page,
    }
    if not args.full_page:
        return params

    metrics = cdp(args, "Page.getLayoutMetrics", {})
    size = find_mapping(metrics, "cssContentSize") or find_mapping(metrics, "contentSize")
    if not size:
        raise RuntimeError("Page.getLayoutMetrics returned no content size")
    width = size.get("width")
    height = size.get("height")
    if not isinstance(width, (int, float)) or not isinstance(height, (int, float)):
        raise RuntimeError("Page.getLayoutMetrics returned invalid content dimensions")
    if width <= 0 or height <= 0:
        raise RuntimeError(f"Invalid content dimensions: {width}x{height}")
    params["clip"] = {"x": 0, "y": 0, "width": width, "height": height, "scale": 1}
    return params


def main() -> int:
    args = parse_args()
    output = args.output.expanduser().resolve()
    if output.exists() and not args.force:
        raise RuntimeError(f"Output already exists: {output}; pass --force to replace it")
    if not output.parent.is_dir():
        raise RuntimeError(f"Output directory does not exist: {output.parent}")

    response = cdp(args, "Page.captureScreenshot", capture_params(args))
    encoded = find_string(response, "data")
    if not encoded:
        raise RuntimeError("Page.captureScreenshot returned no image data")
    try:
        image = base64.b64decode(encoded, validate=True)
    except binascii.Error as error:
        raise RuntimeError("Page.captureScreenshot returned invalid base64") from error
    if not image.startswith(PNG_SIGNATURE):
        raise RuntimeError("Page.captureScreenshot did not return PNG data")

    temporary = output.with_name(f".{output.name}.{os.getpid()}.tmp")
    try:
        temporary.write_bytes(image)
        os.replace(temporary, output)
    finally:
        temporary.unlink(missing_ok=True)
    print(output)
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (OSError, RuntimeError) as error:
        print(f"capture-screenshot: {error}", file=sys.stderr)
        raise SystemExit(1)
