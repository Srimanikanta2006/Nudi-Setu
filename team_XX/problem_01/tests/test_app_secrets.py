from pathlib import Path

from streamlit.testing.v1 import AppTest
def test_chat_converts_automatically_without_llm_controls():
    app_path = Path(__file__).resolve().parents[1] / "app.py"

    app = AppTest.from_file(str(app_path)).run(timeout=15)

    assert not app.exception
    assert not app.error
    assert any("Automatic offline conversion" in item.value for item in app.caption)
    assert not any("Gemini" in item.label or "Gemma" in item.label for item in app.toggle)

    app.text_area(key="input_text").set_value("ಏನ್ರಿ, ಊಟ ಆತೇನ್ರಿ?").run(timeout=15)
    assert any("ಏನು, ಊಟ ಆಯಿತೇ?" in item.value for item in app.markdown)

    app.radio(key="page").set_value("Overview").run()
    metrics = {item.label: item.value for item in app.metric}
    assert metrics["Real collected"] == "0 / 300"
    assert metrics["Public-source pairs"] == "4"
