import csv

from nudisetu import ollama
from nudisetu.retrieval import get_similar_examples


def _write_csv(path, fields, rows):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def test_retrieval_uses_collected_training_rows_only(tmp_path):
    fields = ["dialect", "dialect_text", "standard_text", "source", "synthetic"]
    _write_csv(tmp_path / "data" / "splits" / "train.csv", fields, [
        {"dialect": "Mangaluru", "dialect_text": "ನಾನು ಮನೆಗೆ ಹೋಗ್ತೀನಿ", "standard_text": "ನಾನು ಮನೆಗೆ ಹೋಗುತ್ತೇನೆ", "source": "collected", "synthetic": "false"},
        {"dialect": "Mangaluru", "dialect_text": "ಯಾಕ ಬಂದಿರಿ", "standard_text": "ಯಾಕೆ ಬಂದಿರಿ", "source": "synthetic", "synthetic": "true"},
        {"dialect": "Hubballi-Dharwad", "dialect_text": "ಏನ್ರಿ ಬಂದಿರಿ", "standard_text": "ಏನು ಬಂದಿರಿ", "source": "collected", "synthetic": "false"},
    ])
    examples = get_similar_examples("ನಾನು ಮನೆಗೆ ಹೋಗ್ತೀನಿ", "Mangaluru", root=tmp_path)
    assert examples == [{"dialect_text": "ನಾನು ಮನೆಗೆ ಹೋಗ್ತೀನಿ", "standard_text": "ನಾನು ಮನೆಗೆ ಹೋಗುತ್ತೇನೆ"}]


def test_retrieval_falls_back_only_to_official_examples(tmp_path):
    fields = ["dialect", "dialect_text", "standard_text", "source", "synthetic"]
    _write_csv(tmp_path / "data" / "splits" / "train.csv", fields, [])
    _write_csv(tmp_path / "data" / "dataset.csv", fields, [
        {"dialect": "Uttara Kannada", "dialect_text": "ಹೆಂಗಿದ್ದೀರಿ?", "standard_text": "ಹೇಗಿದ್ದೀರಿ?", "source": "official_example", "synthetic": "false"},
        {"dialect": "Uttara Kannada", "dialect_text": "ಬರ್ತೀನಿ", "standard_text": "ಬರುತ್ತೇನೆ", "source": "synthetic", "synthetic": "true"},
    ])
    assert get_similar_examples("ಹೆಂಗಿದ್ದೀರಿ?", "Uttara Kannada", root=tmp_path) == [
        {"dialect_text": "ಹೆಂಗಿದ್ದೀರಿ?", "standard_text": "ಹೇಗಿದ್ದೀರಿ?"}
    ]


def test_local_model_refines_with_a_rule_fallback_and_examples(monkeypatch):
    captured = {}
    monkeypatch.setattr(ollama, "available_models", lambda: ["gemma4:latest"])

    class Response:
        def raise_for_status(self):
            pass

        def json(self):
            return {"message": {"content": "ನಾನು ಮನೆಗೆ ಹೋಗುತ್ತೇನೆ."}}

    def fake_post(url, **kwargs):
        captured["url"] = url
        captured["body"] = kwargs["json"]
        return Response()

    monkeypatch.setattr(ollama.requests, "post", fake_post)
    output, note = ollama.refine(
        "Mangaluru", "ನಾನು ಮನೆಗೆ ಹೋಗ್ತೀನಿ.", "ನಾನು ಮನೆಗೆ ಹೋಗುತ್ತೇನೆ.",
        examples=[{"dialect_text": "ಬರ್ತೀನಿ", "standard_text": "ಬರುತ್ತೇನೆ"}],
    )
    assert output == "ನಾನು ಮನೆಗೆ ಹೋಗುತ್ತೇನೆ."
    assert "Local gemma4:latest" in note
    assert captured["url"].endswith("/api/chat")
    user_prompt = captured["body"]["messages"][1]["content"]
    assert "ನಾನು ಮನೆಗೆ ಹೋಗ್ತೀನಿ." in user_prompt
    assert "ಬರ್ತೀನಿ → ಬರುತ್ತೇನೆ" in user_prompt


def test_local_model_failure_keeps_rules_draft(monkeypatch):
    monkeypatch.setattr(ollama, "available_models", lambda: ["gemma4:latest"])
    monkeypatch.setattr(ollama.requests, "post", lambda *args, **kwargs: (_ for _ in ()).throw(ollama.requests.Timeout()))
    draft = "ನಾನು ಮನೆಗೆ ಹೋಗುತ್ತೇನೆ."
    output, note = ollama.refine("Mangaluru", "ನಾನು ಮನೆಗೆ ಹೋಗ್ತೀನಿ.", draft)
    assert output == draft
    assert note == "Local model failed; kept offline rules draft"
