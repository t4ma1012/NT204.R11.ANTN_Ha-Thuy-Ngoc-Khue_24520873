import json
from pathlib import Path

from src.preprocessor.preprocessor import Preprocessor


def write_output(path, data):
    output_file = Path(path)
    output_file.parent.mkdir(parents=True, exist_ok=True)

    output_file.write_text(
        json.dumps(
            data,
            indent=2,
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )


def test_normalization():
    preprocessor = Preprocessor()

    event = {
        "timestamp": "2026-09-27T06:21:00Z",
        "protocol": " http ",
        "src_ip": "192.168.001.001",
        "dst_ip": "8.8.8.8",
        "application": {
            "path": " /login ",
            "headers": {
                " Host ": " example.com ",
                "Content-Type": " text/html ",
            },
        },
    }

    result = preprocessor.process(event)

    assert result["protocol"] == "HTTP"

    assert result["src_ip"] == "192.168.001.001"
    assert result["dst_ip"] == "8.8.8.8"

    assert result["application"]["path"] == "/login"

    assert (
        result["application"]["headers"]["host"]
        == "example.com"
    )

    assert (
        result["application"]["headers"]["content-type"]
        == "text/html"
    )

    assert result["preprocess_status"] == "valid"
    assert result["processing_action"] == "normalized"

    write_output(
        "TEST/preprocessor/normalization/output.json",
        result,
    )


def test_missing_field():
    preprocessor = Preprocessor()

    event = {
        "timestamp": "2026-09-27T06:21:00Z",
        "protocol": "TCP",
    }

    result = preprocessor.process(event)

    assert result["src_ip"] is None
    assert result["dst_ip"] is None

    assert result["application"] == {}

    assert result["preprocess_status"] == "partial"
    assert result["processing_action"] == "keep"

    assert "src_ip" in result["reason"]
    assert "dst_ip" in result["reason"]

    write_output(
        "TEST/preprocessor/missing_field/output.json",
        result,
    )