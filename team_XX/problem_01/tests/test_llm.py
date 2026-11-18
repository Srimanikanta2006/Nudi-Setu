from nudisetu import llm


def test_llm_without_key_returns_rule_draft(monkeypatch):
    monkeypatch.delenv("GEMINI_API_KEY", raising=False)
    draft = "ಕನ್ನಡ ವಾಕ್ಯ"
    output, note = llm.refine("Mangaluru", draft)
    assert output == draft
    assert "not configured" in note


def test_llm_uses_active_model_and_accepts_kannada(monkeypatch, tmp_path):
    monkeypatch.delenv("GEMINI_API_KEY", raising=False)
    monkeypatch.setenv("NUDISETU_CACHE_DIR", str(tmp_path))
    captured = {}

    class Response:
        def raise_for_status(self):
            pass

        def json(self):
            return {"candidates": [{"content": {"parts": [{"text": "ಇದು ಕನ್ನಡ ವಾಕ್ಯ."}]}}]}

    def fake_post(url, **kwargs):
        captured["url"] = url
        return Response()

    monkeypatch.setattr(llm.requests, "post", fake_post)
    output, note = llm.refine("Mangaluru", "ಕನ್ನಡ draft", api_key="test-key")
    assert "/models/gemini-3.6-flash:generateContent" in captured["url"]
    assert "key=test-key" in captured["url"]
    assert output == "ಇದು ಕನ್ನಡ ವಾಕ್ಯ."
    assert note == "LLM refined"


def test_llm_api_failure_falls_back_without_raising(monkeypatch, tmp_path):
    monkeypatch.delenv("GEMINI_API_KEY", raising=False)
    monkeypatch.setenv("NUDISETU_CACHE_DIR", str(tmp_path))
    monkeypatch.setattr(llm.requests, "post", lambda *args, **kwargs: (_ for _ in ()).throw(llm.requests.RequestException("offline")))
    monkeypatch.setattr(llm.time, "sleep", lambda _: None)
    draft = "ಕನ್ನಡ draft"
    output, note = llm.refine("Mangaluru", draft, api_key="test-key")
    assert output == draft
    assert note == "LLM fallback: RequestException"
