from pathlib import Path

from edge_reader.bundle import pack_bundle, read_bundle, unpack_bundle, write_document_text, write_manifest, write_timings
from edge_reader.models import SentenceSpan


def test_pack_and_read_bundle_roundtrip(tmp_path: Path):
    workdir = tmp_path / "work"
    workdir.mkdir()
    (workdir / "audio").mkdir()
    (workdir / "audio" / "000000.mp3").write_bytes(b"fake")

    sentences = [SentenceSpan(0, 0, 12, "Hello world.")]
    write_document_text(workdir, "Hello world.")
    write_manifest(
        workdir,
        title="Demo",
        source_name="demo.txt",
        voice="en-US-AriaNeural",
        locale="en-US",
        rate="+0%",
        sentences=sentences,
    )
    write_timings(
        workdir,
        [
            {
                "sentence_index": 0,
                "audio": "audio/000000.mp3",
                "events": [
                    {"type": "WordBoundary", "offset_ms": 0, "duration_ms": 200, "text": "Hello"}
                ],
            }
        ],
    )

    bundle = pack_bundle(workdir, tmp_path / "demo.edgevoice.zip")
    unpacked = unpack_bundle(bundle)
    manifest, timings, text = read_bundle(unpacked)

    assert manifest["title"] == "Demo"
    assert manifest["sentences"][0]["text"] == "Hello world."
    assert timings["segments"][0]["events"][0]["text"] == "Hello"
    assert text == "Hello world."
