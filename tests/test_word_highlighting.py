"""Tests for word-level highlighting feature."""

from edge_reader.models import SentenceSpan


def test_word_boundary_parsing():
    """Test that word boundaries are correctly parsed from timing data."""
    timings = {
        "schema_version": 1,
        "timing_units": "milliseconds",
        "segments": [
            {
                "sentence_index": 0,
                "audio": "audio/000000.mp3",
                "events": [
                    {
                        "type": "WordBoundary",
                        "offset_ms": 0,
                        "duration_ms": 200,
                        "text": "Hello",
                    },
                    {
                        "type": "WordBoundary",
                        "offset_ms": 200,
                        "duration_ms": 150,
                        "text": "world",
                    },
                    {
                        "type": "SentenceBoundary",
                        "offset_ms": 350,
                        "duration_ms": 0,
                        "text": "",
                    },
                ],
            },
        ],
    }

    # Simulate word boundary parsing
    word_boundaries = {}
    segments = timings.get("segments", [])

    for segment in segments:
        sentence_index = segment.get("sentence_index", -1)
        if sentence_index < 0:
            continue

        words = [
            event for event in segment.get("events", [])
            if event.get("type") == "WordBoundary"
        ]

        if words:
            word_boundaries[sentence_index] = words

    assert 0 in word_boundaries
    assert len(word_boundaries[0]) == 2
    assert word_boundaries[0][0]["text"] == "Hello"
    assert word_boundaries[0][0]["offset_ms"] == 0
    assert word_boundaries[0][0]["duration_ms"] == 200
    assert word_boundaries[0][1]["text"] == "world"
    assert word_boundaries[0][1]["offset_ms"] == 200
    assert word_boundaries[0][1]["duration_ms"] == 150


def test_word_position_matching():
    """Test finding current word position within a sentence."""
    sentence_text = "Hello world"
    sentence_span = SentenceSpan(index=0, start=0, end=11, text=sentence_text)

    # Word boundary event
    word_event = {
        "type": "WordBoundary",
        "offset_ms": 200,
        "duration_ms": 150,
        "text": "world",
    }

    word_text = word_event.get("text", "")
    word_start = sentence_text.find(word_text)
    word_end = word_start + len(word_text)

    assert word_start == 6
    assert word_end == 11

    # Convert to document-level positions
    doc_word_start = sentence_span.start + word_start
    doc_word_end = sentence_span.start + word_end

    assert doc_word_start == 6
    assert doc_word_end == 11


def test_word_event_selection_by_position():
    """Test selecting correct word based on playback position."""
    boundaries = [
        {
            "type": "WordBoundary",
            "offset_ms": 0,
            "duration_ms": 200,
            "text": "Hello",
        },
        {
            "type": "WordBoundary",
            "offset_ms": 200,
            "duration_ms": 150,
            "text": "world",
        },
        {
            "type": "WordBoundary",
            "offset_ms": 350,
            "duration_ms": 100,
            "text": "test",
        },
    ]

    # Test position 50 (within "Hello")
    pos_ms = 50
    current_word = None
    for boundary in boundaries:
        start = boundary.get("offset_ms", 0)
        duration = boundary.get("duration_ms", 0)
        end = start + duration

        if start <= pos_ms < end:
            current_word = boundary
            break

    assert current_word is not None
    assert current_word["text"] == "Hello"

    # Test position 250 (within "world")
    pos_ms = 250
    current_word = None
    for boundary in boundaries:
        start = boundary.get("offset_ms", 0)
        duration = boundary.get("duration_ms", 0)
        end = start + duration

        if start <= pos_ms < end:
            current_word = boundary
            break

    assert current_word is not None
    assert current_word["text"] == "world"

    # Test position 400 (within "test")
    pos_ms = 400
    current_word = None
    for boundary in boundaries:
        start = boundary.get("offset_ms", 0)
        duration = boundary.get("duration_ms", 0)
        end = start + duration

        if start <= pos_ms < end:
            current_word = boundary
            break

    assert current_word is not None
    assert current_word["text"] == "test"

    # Test position 500 (after "test", no match)
    pos_ms = 500
    current_word = None
    for boundary in boundaries:
        start = boundary.get("offset_ms", 0)
        duration = boundary.get("duration_ms", 0)
        end = start + duration

        if start <= pos_ms < end:
            current_word = boundary
            break

    assert current_word is None


def test_multiple_sentences_with_boundaries():
    """Test parsing multiple sentences each with word boundaries."""
    timings = {
        "schema_version": 1,
        "timing_units": "milliseconds",
        "segments": [
            {
                "sentence_index": 0,
                "audio": "audio/000000.mp3",
                "events": [
                    {
                        "type": "WordBoundary",
                        "offset_ms": 0,
                        "duration_ms": 100,
                        "text": "First",
                    },
                    {
                        "type": "WordBoundary",
                        "offset_ms": 100,
                        "duration_ms": 150,
                        "text": "sentence",
                    },
                ],
            },
            {
                "sentence_index": 1,
                "audio": "audio/000001.mp3",
                "events": [
                    {
                        "type": "WordBoundary",
                        "offset_ms": 0,
                        "duration_ms": 120,
                        "text": "Second",
                    },
                    {
                        "type": "WordBoundary",
                        "offset_ms": 120,
                        "duration_ms": 130,
                        "text": "sentence",
                    },
                ],
            },
        ],
    }

    word_boundaries = {}
    segments = timings.get("segments", [])

    for segment in segments:
        sentence_index = segment.get("sentence_index", -1)
        if sentence_index < 0:
            continue

        words = [
            event for event in segment.get("events", [])
            if event.get("type") == "WordBoundary"
        ]

        if words:
            word_boundaries[sentence_index] = words

    assert 0 in word_boundaries
    assert 1 in word_boundaries
    assert len(word_boundaries[0]) == 2
    assert len(word_boundaries[1]) == 2
    assert word_boundaries[0][0]["text"] == "First"
    assert word_boundaries[1][0]["text"] == "Second"
