from __future__ import annotations

import json
import shutil
import tempfile
import zipfile
from dataclasses import asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .models import SentenceSpan

SCHEMA_VERSION = 1


class BundleError(RuntimeError):
    pass


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def create_workdir() -> Path:
    return Path(tempfile.mkdtemp(prefix="edge_reader_bundle_"))


def write_manifest(
    workdir: Path,
    *,
    title: str,
    source_name: str,
    voice: str,
    locale: str,
    rate: str,
    sentences: list[SentenceSpan],
) -> dict[str, Any]:
    manifest: dict[str, Any] = {
        "schema_version": SCHEMA_VERSION,
        "created_at": utc_now_iso(),
        "engine": "edge-tts",
        "title": title,
        "source_name": source_name,
        "voice": voice,
        "locale": locale,
        "rate": rate,
        "sentence_count": len(sentences),
        "sentences": [
            {
                "index": s.index,
                "start": s.start,
                "end": s.end,
                "text": s.text,
                "audio": f"audio/{s.index:06d}.mp3",
            }
            for s in sentences
        ],
    }
    (workdir / "manifest.json").write_text(json.dumps(manifest, indent=2, ensure_ascii=False), encoding="utf-8")
    return manifest


def write_document_text(workdir: Path, text: str) -> None:
    (workdir / "document.txt").write_text(text, encoding="utf-8")


def write_timings(workdir: Path, segments: list[dict[str, Any]]) -> None:
    data = {
        "schema_version": SCHEMA_VERSION,
        "timing_units": "milliseconds",
        "segments": segments,
    }
    (workdir / "timings.json").write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")


def pack_bundle(workdir: Path, bundle_path: str | Path) -> Path:
    out = Path(bundle_path).expanduser().resolve()
    if out.suffix.lower() != ".zip":
        out = out.with_suffix(out.suffix + ".zip") if out.suffix else out.with_suffix(".edgevoice.zip")
    out.parent.mkdir(parents=True, exist_ok=True)

    with zipfile.ZipFile(out, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        for item in sorted(workdir.rglob("*")):
            if item.is_file():
                zf.write(item, item.relative_to(workdir).as_posix())
    return out


def unpack_bundle(bundle_path: str | Path) -> Path:
    source = Path(bundle_path).expanduser().resolve()
    if not source.exists():
        raise BundleError(f"Bundle does not exist: {source}")
    workdir = create_workdir()
    try:
        with zipfile.ZipFile(source, "r") as zf:
            names = set(zf.namelist())
            required = {"manifest.json", "timings.json", "document.txt"}
            missing = required - names
            if missing:
                raise BundleError(f"Bundle is missing: {', '.join(sorted(missing))}")
            zf.extractall(workdir)
        return workdir
    except Exception:
        shutil.rmtree(workdir, ignore_errors=True)
        raise


def read_bundle(workdir: str | Path) -> tuple[dict[str, Any], dict[str, Any], str]:
    wd = Path(workdir)
    try:
        manifest = json.loads((wd / "manifest.json").read_text(encoding="utf-8"))
        timings = json.loads((wd / "timings.json").read_text(encoding="utf-8"))
        text = (wd / "document.txt").read_text(encoding="utf-8")
    except Exception as exc:
        raise BundleError(f"Could not read bundle at {wd}") from exc

    if manifest.get("schema_version") != SCHEMA_VERSION:
        raise BundleError(f"Unsupported bundle schema: {manifest.get('schema_version')}")
    return manifest, timings, text


def copy_or_replace(src: Path, dst: Path) -> None:
    dst.parent.mkdir(parents=True, exist_ok=True)
    if dst.exists():
        dst.unlink()
    shutil.copy2(src, dst)
