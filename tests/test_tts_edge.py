from edge_reader.tts_edge import rate_percent_to_edge


def test_rate_percent_formatting_and_clamping():
    assert rate_percent_to_edge(0) == "+0%"
    assert rate_percent_to_edge(15) == "+15%"
    assert rate_percent_to_edge(-20) == "-20%"
    assert rate_percent_to_edge(-999) == "-90%"
    assert rate_percent_to_edge(999) == "+200%"
