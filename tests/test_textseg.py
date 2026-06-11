from edge_reader.textseg import normalize_document_text, split_sentences


def test_split_basic_sentences_preserves_spans():
    text = "Hello world. This is a test! Is it working? Yes."
    spans = split_sentences(text)
    assert [s.text for s in spans] == [
        "Hello world.",
        "This is a test!",
        "Is it working?",
        "Yes.",
    ]
    for span in spans:
        assert text[span.start : span.end] == span.text


def test_abbreviations_and_decimals_do_not_split():
    text = "Dr. Smith measured 3.3 volts. It worked at 5.0 volts too."
    spans = split_sentences(text)
    assert [s.text for s in spans] == [
        "Dr. Smith measured 3.3 volts.",
        "It worked at 5.0 volts too.",
    ]


def test_paragraph_fallback_for_headings():
    text = "Chapter One\n\nThis paragraph has a sentence."
    spans = split_sentences(text)
    assert [s.text for s in spans] == ["Chapter One", "This paragraph has a sentence."]


def test_normalize_document_text():
    assert normalize_document_text("a\r\nb\r\rc\t \n") == "a\nb\n\nc\n"
