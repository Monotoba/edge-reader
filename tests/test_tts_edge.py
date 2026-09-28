from edge_reader.tts_edge import _event_to_ms, rate_percent_to_edge


def test_event_offset_conversion_and_bad_values():
    assert _event_to_ms(25_000) == 2
    assert _event_to_ms("100000") == 10
    assert _event_to_ms(None) == 0
    assert _event_to_ms("invalid") == 0


def test_rate_percent_formatting_and_clamping():
    assert rate_percent_to_edge(0) == "+0%"
    assert rate_percent_to_edge(15) == "+15%"
    assert rate_percent_to_edge(-20) == "-20%"
    assert rate_percent_to_edge(-999) == "-90%"
    assert rate_percent_to_edge(999) == "+200%"
