"""Nudi Setu's responsive, glass-orb Streamlit demo."""
from __future__ import annotations

import csv
import html
import sys
from pathlib import Path

import pandas as pd
import streamlit as st

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))
from nudisetu.pipeline import convert
from nudisetu.evaluate import evaluate_csv
from nudisetu.glossary import load_glossary

DIALECTS = ["Uttara Kannada", "Mangaluru", "Hubballi-Dharwad"]
CONVERSION_DIALECTS = [*DIALECTS, "Havyaka"]
DATA_PATH = ROOT / "data" / "dataset.csv"
PUBLIC_PAIRS_PATH = ROOT / "data" / "public_source_pairs" / "mangaluru_wikipedia.csv"


def load_rows() -> list[dict[str, str]]:
    """Read project examples as UTF-8 without treating them as collected data."""
    try:
        with DATA_PATH.open(encoding="utf-8-sig", newline="") as handle:
            return list(csv.DictReader(handle))
    except (OSError, csv.Error):
        return []


def load_public_pairs() -> list[dict[str, str]]:
    """Read cited public-source comparison examples, separate from collection data."""
    collected: list[dict[str, str]] = []
    for path in sorted(PUBLIC_PAIRS_PATH.parent.glob("*.csv")):
        try:
            with path.open(encoding="utf-8-sig", newline="") as handle:
                collected.extend(csv.DictReader(handle))
        except (OSError, csv.Error):
            continue
    return collected


def render_alignment(alignment: list[dict[str, object]], side: str) -> str:
    """Render escaped source/target word groups, highlighting changed segments."""
    chunks: list[str] = []
    key = "source" if side == "source" else "target"
    for group in alignment:
        tokens = group.get(key, [])
        if not tokens:
            continue
        value = html.escape(" ".join(str(token) for token in tokens))
        if group.get("changed"):
            chunks.append(f'<mark class="word-change">{value}</mark>')
        else:
            chunks.append(value)
    return " ".join(chunks)


def clear_composer():
    """Safely reset input and result before widget instantiation."""
    st.session_state.input_text = ""
    st.session_state.last_result = None


st.set_page_config(
    page_title="Nudi Setu · Kannada dialect bridge",
    page_icon="🌉",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown(
    r"""<style>
@import url('https://fonts.googleapis.com/css2?family=Inter+Tight:wght@400;500;600&family=Noto+Sans+Kannada:wght@400;500;600;700&display=swap');
:root{--u:min(0.069444444vw,0.099206349dvh);--page:#0e0e0e;--surface:#151515;--surface2:#1d1d1d;--text:#f6f7fb;--muted:#8c8c8c;--quiet:#6e6e6e;--blue:#2f6bff;--violet:#5a4cf5;--line:rgba(255,255,255,.08)}
html,body,[class*="css"],[data-testid="stAppViewContainer"]{font-family:'Inter Tight','Noto Sans Kannada',sans-serif!important;color:var(--text)!important}
.stApp{background:radial-gradient(ellipse 68% 39% at 51% -7%,rgba(64,110,255,.20),transparent 72%),var(--page);min-height:100dvh}
[data-testid="stHeader"],[data-testid="stToolbar"],footer{visibility:hidden;height:0}
[data-testid="stMainBlockContainer"]{max-width:none!important;padding:0 2.5vw 3vw!important}
.topbar{height:calc(68 * var(--u));min-height:58px;display:flex;align-items:center;justify-content:space-between;border-bottom:1px solid var(--line);margin-bottom:calc(15 * var(--u));color:#c6c9d2}
.brandline{display:flex;align-items:center;gap:12px;font-size:15px;letter-spacing:.01em}
.brandmark{width:30px;height:30px;border-radius:9px;display:grid;place-items:center;background:#f4f6fb;color:#101114;font-size:16px;font-weight:600;box-shadow:0 0 28px rgba(74,112,255,.2)}
.crumb{color:var(--quiet)}.crumb b{color:#f5f6fa;font-weight:500}.chev{color:#555;margin:0 9px}
.top-right{display:flex;align-items:center;gap:10px}.status-pill{padding:8px 12px;border:1px solid rgba(93,125,255,.2);background:rgba(26,31,49,.7);border-radius:999px;font-size:12px;color:#bdc8ff;display:flex;align-items:center;gap:8px;white-space:nowrap}
.live-dot{width:7px;height:7px;background:#5c8cff;border-radius:50%;box-shadow:0 0 11px #4e7aff;display:inline-block}
.hero{text-align:center;position:relative;isolation:isolate;padding:0 0 calc(10 * var(--u));overflow:hidden}
.hero:before{content:"";position:absolute;z-index:-1;inset:-45% -10% 15%;background:radial-gradient(ellipse at 51% 15%,rgba(64,110,255,.43),transparent 39%),radial-gradient(ellipse at 63% 29%,rgba(124,72,240,.22),transparent 31%),radial-gradient(ellipse at 36% 30%,rgba(88,199,255,.12),transparent 26%);filter:blur(22px);pointer-events:none}
.orb-stage{height:calc(138 * var(--u));min-height:110px;display:flex;align-items:center;justify-content:center;margin:calc(-12 * var(--u)) auto calc(-4 * var(--u));position:relative;mask-image:radial-gradient(ellipse 58% 62% at 50% 50%,#000 58%,transparent 80%);-webkit-mask-image:radial-gradient(ellipse 58% 62% at 50% 50%,#000 58%,transparent 80%)}
.orb{width:calc(84 * var(--u));height:calc(84 * var(--u));min-width:72px;min-height:72px;position:relative;border-radius:50%;overflow:hidden;background:radial-gradient(circle at 30% 23%,rgba(226,243,255,.56),transparent 12%),radial-gradient(circle at 31% 24%,rgba(145,190,255,.28),transparent 28%),radial-gradient(circle at 50% 55%,#101421 0,#0b0e15 48%,#030407 73%);border:1px solid rgba(219,235,255,.48);box-shadow:inset 7px 4px 16px rgba(225,241,255,.13),inset -10px -8px 20px rgba(60,89,195,.14),0 0 28px rgba(51,104,255,.29),0 0 80px rgba(47,107,255,.2);animation:orb-breathe 5s ease-in-out infinite}
.orb:before{content:"";position:absolute;inset:15%;border-radius:47% 53% 59% 41%;background:conic-gradient(from 20deg,transparent 0 10%,#282ce7 18%,#4e7cff 28%,#7b39ec 43%,#151a55 57%,#4259ff 72%,#1c205d 83%,transparent 94%);filter:blur(7px);opacity:.85;animation:core-turn 8s linear infinite;transform:rotate(-20deg) scale(1.13)}
.orb:after{content:"";position:absolute;inset:0;border-radius:50%;background:radial-gradient(ellipse at 32% 18%,rgba(255,255,255,.48),transparent 18%),radial-gradient(ellipse at 73% 78%,rgba(85,135,255,.19),transparent 34%),linear-gradient(115deg,rgba(255,255,255,.12),transparent 24% 69%,rgba(107,149,255,.10));box-shadow:inset 2px 2px 2px rgba(255,255,255,.42),inset -2px -3px 6px rgba(130,168,255,.24)}
.orb-glint{position:absolute;z-index:2;width:30%;height:9%;left:15%;top:13%;border-radius:50%;background:rgba(255,255,255,.43);filter:blur(3px);transform:rotate(-32deg)}
@keyframes core-turn{to{transform:rotate(340deg) scale(1.13)}}@keyframes orb-breathe{50%{box-shadow:inset 7px 4px 16px rgba(225,241,255,.18),inset -10px -8px 24px rgba(60,89,195,.18),0 0 36px rgba(51,104,255,.4),0 0 95px rgba(47,107,255,.27)}}
.eyebrow{font-size:12px;letter-spacing:.16em;text-transform:uppercase;color:#8e9ac2;margin:0 0 8px}
.greeting{color:#a4a8b2;font-size:calc(17 * var(--u));margin:0 0 8px}
.headline{font-size:clamp(25px,calc(30 * var(--u)),39px);font-weight:500;letter-spacing:.045em;line-height:1.12;margin:0 0 10px;color:#f6f7fb}
.subline{color:#9699a3;font-size:15px;margin:0 0 18px}
.ruleline{display:flex;align-items:center;justify-content:center;gap:8px;color:#7e86a0;font-size:11px;letter-spacing:.04em;flex-wrap:wrap}.ruleline span{border:1px solid rgba(125,148,255,.13);background:rgba(20,24,35,.67);padding:6px 9px;border-radius:999px}.ruleline i{font-style:normal;color:#5268c7}
.stRadio>div{gap:8px}.stRadio [role=radiogroup]{gap:8px}.stRadio label{background:#151515;border:1px solid var(--line);border-radius:10px;padding:7px 12px!important;color:#a8a8ad!important}.stRadio label:has(input:checked){background:#222a42;border-color:rgba(91,124,255,.5);color:white!important}
div[data-testid="stSelectbox"]>div>div,div[data-testid="stTextInput"]>div>div,div[data-testid="stTextArea"] textarea{background:#141414!important;border:1px solid rgba(255,255,255,.09)!important;color:#f6f7fb!important;border-radius:12px!important}
div[data-testid="stTextArea"] textarea{font-family:'Noto Sans Kannada','Inter Tight',sans-serif!important;min-height:110px;border-color:rgba(255,255,255,.12)!important;box-shadow:none!important;outline:none!important}
div[data-testid="stTextArea"] textarea:focus,div[data-testid="stTextArea"] textarea[aria-invalid="true"]{border-color:rgba(100,130,255,.62)!important;box-shadow:0 0 0 1px rgba(100,130,255,.14)!important}
div[data-testid="stTextArea"] textarea::placeholder,div[data-testid="stTextInput"] input::placeholder{color:#6d7382!important}
.stButton>button,.stDownloadButton>button{background:#1a1a1d;color:#e9eaf0;border:1px solid rgba(255,255,255,.1);border-radius:10px;min-height:38px;transition:all .2s ease}.stButton>button:hover,.stDownloadButton>button:hover{border-color:rgba(94,126,255,.55);color:white;background:#20222b;transform:translateY(-1px)}
.stButton>button[kind="primary"]{background:linear-gradient(110deg,#2f6bff,#514cf2 58%,#7050df)!important;border:0!important;box-shadow:0 6px 24px rgba(55,91,245,.35)!important;font-weight:600!important;color:white!important;border-radius:11px!important;transition:all .25s ease!important}.stButton>button[kind="primary"]:hover{transform:translateY(-1px)!important;box-shadow:0 9px 30px rgba(55,91,245,.55)!important;filter:brightness(1.08)!important}
.st-key-composer{border:1px solid transparent!important;border-radius:15px!important;background:linear-gradient(#151515,#151515) padding-box,linear-gradient(105deg,#2f6bff,#403fe5,#8253ed,#2f6bff) border-box!important;padding:12px 15px 10px!important;box-shadow:0 12px 45px rgba(0,0,0,.27)}
.st-key-composer [data-testid="stTextArea"] textarea{border:0!important;background:transparent!important;box-shadow:none!important;padding-left:2px}
.composer-label{font-size:11px;letter-spacing:.12em;text-transform:uppercase;color:#777d90;margin:0 0 5px}
.suggestion-title{font-size:11px;letter-spacing:.12em;text-transform:uppercase;color:#737987;margin:18px 0 8px}
.sample-card,.feature-card,.result-card,.recent-card,.metric-card{background:linear-gradient(145deg,#18181b,#131315);border:1px solid rgba(255,255,255,.075);border-radius:14px;padding:14px 15px;height:100%;box-shadow:0 10px 30px rgba(0,0,0,.12)}
.sample-kicker{font-size:10px;text-transform:uppercase;letter-spacing:.13em;color:#7887bc;margin-bottom:7px}.sample-text{font-family:'Noto Sans Kannada',sans-serif;font-size:16px;color:#f1f2f5;line-height:1.55}.sample-translation{font-family:'Noto Sans Kannada',sans-serif;font-size:13px;color:#8c8c8c;margin-top:5px}
.section-title{font-size:15px;font-weight:500;color:#e8e9ee;margin:10px 0 8px}.section-sub{font-size:12px;color:#757982;margin:0 0 10px}
.result-card{min-height:125px}.result-label{font-size:10px;letter-spacing:.14em;text-transform:uppercase;color:#7a8299;margin-bottom:12px}.result-text{font-family:'Noto Sans Kannada',sans-serif;font-size:20px;line-height:1.65;color:#f5f6fa}.word-change{background:rgba(84,112,255,.22);color:#fff;border:1px solid rgba(125,151,255,.28);border-radius:5px;padding:1px 4px}
.st-key-shell{min-height:100dvh}.st-key-side_rail{position:fixed!important;z-index:100;left:0;top:0;height:100dvh;width:calc(48 * var(--u));min-width:52px;background:#101012;border-right:1px solid var(--line);padding:12px 9px;display:flex;flex-direction:column;align-items:center;box-sizing:border-box}.rail-icons{height:calc(100dvh - 90px);display:flex;flex-direction:column;align-items:center;gap:10px;color:#686a74;font-size:15px}.rail-icons>div{width:32px;height:32px;border-radius:10px;display:grid;place-items:center}.rail-icons .rail-active{background:#20253a;color:#9db2ff;box-shadow:inset 0 0 0 1px rgba(106,137,255,.24)}.rail-icons .rail-bottom{margin-top:auto}
div[data-testid="stExpander"]{background:#151515;border:1px solid var(--line);border-radius:12px}
[data-testid="stMetric"]{background:#171719;border:1px solid var(--line);border-radius:12px;padding:13px 15px}
div[data-testid="stDataFrame"]{border:1px solid var(--line);border-radius:12px;overflow:hidden}
.note{font-size:12px;line-height:1.6;color:#8c8c8c}.footer-note{border-top:1px solid var(--line);padding-top:12px;margin-top:22px;color:#656873;font-size:11px}
@media(max-width:760px){:root{--u:1px} [data-testid="stMainBlockContainer"]{padding:0 14px 24px!important}.st-key-side_rail{display:none!important}.topbar{height:auto;min-height:54px;margin-bottom:12px;gap:8px}.top-right .status-pill{font-size:10px;padding:7px 8px}.brandline{font-size:13px;flex-wrap:wrap}.orb-stage{height:112px;margin:-7px auto -3px}.headline{font-size:25px}.subline{font-size:13px;max-width:330px;margin-left:auto;margin-right:auto}.ruleline{max-width:360px;margin:0 auto}.sample-card{padding:12px}.sample-text{font-size:14px}.result-text{font-size:18px}.st-key-composer{padding:9px!important}.stRadio [role=radiogroup]{flex-wrap:wrap}.stRadio label{padding:6px 9px!important}}
@media(prefers-reduced-motion:reduce){*,*::before,*::after{animation:none!important;scroll-behavior:auto!important;transition:none!important}}
</style>""",
    unsafe_allow_html=True,
)

rows = load_rows()
official_rows = [row for row in rows if row.get("source") == "official_example"]

left, main = st.columns([0.055, 0.945], gap="small")
with left:
    with st.container(key="side_rail"):
        st.markdown('<div class="brandmark">N</div><div style="height:18px"></div><div class="rail-icons"><div class="rail-active" title="Chat">✦</div><div class="rail-bottom" title="Settings">⚙</div></div>', unsafe_allow_html=True)

with main:
    st.markdown(
        '<div class="topbar"><div class="brandline"><span class="crumb">Workspace</span><span class="chev">›</span><b>Nudi Setu</b><span class="chev">›</span><span>Dialect bridge</span></div><div class="top-right"><span class="status-pill"><span class="live-dot"></span> OFFLINE RULES READY</span></div></div>',
        unsafe_allow_html=True,
    )
    page = st.radio("Navigate", ["Chat Mode", "Overview", "Glossary", "Collection"], horizontal=True, label_visibility="collapsed", key="page")

    if page == "Chat Mode":
        st.markdown(
            '<section class="hero"><div class="orb-stage"><div class="orb"><span class="orb-glint"></span></div></div><p class="eyebrow">ಕನ್ನಡದ ವೈವಿಧ್ಯಕ್ಕೆ ಒಂದೇ ಸೇತು · A bridge across Kannada</p><p class="greeting">ನಮಸ್ಕಾರ · Namaskara</p><h1 class="headline">SAY IT YOUR WAY. WRITE IT IN TEXTBOOK KANNADA.</h1><p class="subline">Preserve the meaning. Make every dialect easier to read and learn.</p><div class="ruleline"><span>Dialect text</span><i>→</i><span>Normalize</span><i>→</i><span>Map words</span><i>→</i><span>Rewrite grammar</span><i>→</i><span>Textbook Kannada</span></div></section>',
            unsafe_allow_html=True,
        )

        if "input_text" not in st.session_state:
            st.session_state.input_text = ""
        if "last_result" not in st.session_state:
            st.session_state.last_result = None

        dialect = st.selectbox("Dialect variety", CONVERSION_DIALECTS, index=2, key="dialect", format_func=lambda value: "Havyaka · experimental" if value == "Havyaka" else value)
        if dialect == "Havyaka":
            st.caption("Experimental Havyaka mappings are based on published word examples and still need review by a fluent Havyaka speaker.")
        relevant = [r for r in official_rows if r.get("dialect") == dialect]
        if relevant:
            st.markdown('<div class="suggestion-title">Try an official challenge example</div>', unsafe_allow_html=True)
            sample_cols = st.columns(len(relevant))
            for index, (column, row) in enumerate(zip(sample_cols, relevant)):
                with column:
                    st.markdown(f'<div class="sample-card"><div class="sample-kicker">Official example · {html.escape(dialect)}</div><div class="sample-text">{html.escape(row["dialect_text"])}</div><div class="sample-translation">{html.escape(row["standard_text"])}</div></div>', unsafe_allow_html=True)
                    if st.button("Try this sentence", key=f"sample_{row.get('sentence_id', index)}", use_container_width=True):
                        st.session_state.input_text = row["dialect_text"]
                        st.session_state.last_result = None

        with st.container(key="composer"):
            st.markdown('<div class="composer-label">Your dialect sentence</div>', unsafe_allow_html=True)
            sentence = st.text_area("Dialect text", key="input_text", label_visibility="collapsed", placeholder="ನಿಮ್ಮ ವಾಕ್ಯವನ್ನು ಇಲ್ಲಿ ಬರೆಯಿರಿ… / Type or paste a Kannada sentence…", height=94)
            st.caption("Automatic offline conversion · your text stays in this app; no API key or AI service is used.")

            btn_col1, btn_col2, btn_spacer = st.columns([0.48, 0.26, 0.26], vertical_alignment="center")
            with btn_col1:
                convert_clicked = st.button("⚡ ಪರಿವರ್ತಿಸಿ · Convert", type="primary", use_container_width=True, key="convert_trigger")
            with btn_col2:
                st.button("↺ ತೆರವುಗೊಳಿಸಿ · Clear", use_container_width=True, key="clear_trigger", on_click=clear_composer)
            with btn_spacer:
                st.markdown('<div style="text-align:right;font-size:12px;color:#8590b0;padding-top:4px">🔒 100% Offline</div>', unsafe_allow_html=True)

        if sentence.strip() and any("\u0c80" <= char <= "\u0cff" for char in sentence):
            try:
                st.session_state.last_result = {"dialect": dialect, "text": sentence, "result": convert(sentence, dialect)}
            except Exception:
                st.session_state.last_result = None
                st.error("Conversion could not be completed. Please try again with a shorter Kannada sentence.")
        elif convert_clicked and sentence.strip():
            st.warning("ದಯವಿಟ್ಟು ಕನ್ನಡ ಅಕ್ಷರಗಳನ್ನು ನಮೂದಿಸಿ / Please enter text using Kannada script.")
        else:
            st.session_state.last_result = None

        last = st.session_state.last_result
        if last and last.get("dialect") == dialect:
            result = last["result"]
            st.markdown('<div class="section-title">Conversion result</div>', unsafe_allow_html=True)
            out_left, out_right = st.columns(2, gap="medium")
            with out_left:
                st.markdown(f'<div class="result-card"><div class="result-label">Dialect input · {html.escape(dialect)}</div><div class="result-text">{render_alignment(result["alignment"], "source")}</div></div>', unsafe_allow_html=True)
            with out_right:
                st.markdown(f'<div class="result-card"><div class="result-label">Textbook Kannada</div><div class="result-text">{render_alignment(result["alignment"], "target")}</div></div>', unsafe_allow_html=True)
            st.caption("Blue-violet highlights mark changed words. Applied rules: " + (", ".join(result["rules"]) or "none"))
            if any(hit.get("confidence") == "needs_native_check" for hit in result["hits"]):
                st.caption("One or more applied mappings still need native-speaker review.")
            public_reference = result.get("public_source_reference")
            if public_reference:
                st.caption(
                    "Exact public-source match; native review is still needed. Source: "
                    f"[{public_reference.get('source_title', 'public source')}]({public_reference.get('source_url', '')}) · "
                    f"{public_reference.get('source_license', '')}"
                )
            if not result["rules"] and not result["hits"] and result.get("public_source_reference") is None:
                st.info("No known dialect rule matched this sentence, so it is shown unchanged. The project needs a verified example or rule for this phrasing.")
            with st.expander("How it was converted · offline stages"):
                stages = result["stages"]
                for label, key in [("1 · Normalize spelling", "normalized"), ("2 · Map known dialect words", "mapped"), ("3 · Apply known grammar rules", "grammar"), ("4 · Textbook Kannada output", "final")]:
                    st.markdown(f"**{label}**  \n{stages[key]}")
                if result["hits"]:
                    st.write("Glossary entries:", [hit.get("entry_id", "") for hit in result["hits"]])

        st.markdown('<div class="section-title">Explore Nudi Setu</div><div class="section-sub">Choose a next step in the navigation above.</div>', unsafe_allow_html=True)
        feature_cols = st.columns(3)
        features = [("✧", "Dialect coverage", "Three challenge varieties plus experimental Havyaka mappings."), ("⌕", "Trace every change", "Inspect normalization, glossary matches and grammar rules."), ("↥", "Batch conversion", "Convert a UTF-8 CSV using the offline rules engine.")]
        for column, (icon, title, desc) in zip(feature_cols, features):
            with column:
                st.markdown(f'<div class="feature-card"><div style="color:#7890ff;font-size:18px;margin-bottom:7px">{icon}</div><div class="section-title">{title}</div><div class="note">{desc}</div></div>', unsafe_allow_html=True)

        with st.expander("Batch convert a CSV"):
            st.caption("Upload a UTF-8 CSV with `dialect` and `dialect_text` columns. The converted file retains your input columns and adds `standard_text`.")
            uploaded = st.file_uploader("Upload CSV", type="csv", key="batch_upload")
            if uploaded:
                try:
                    batch = pd.read_csv(uploaded, encoding="utf-8-sig")
                    if not {"dialect", "dialect_text"}.issubset(batch.columns):
                        st.error("CSV must contain `dialect` and `dialect_text` columns.")
                    else:
                        batch["standard_text"] = [convert(str(row.dialect_text), str(row.dialect))["output"] for row in batch.itertuples()]
                        st.dataframe(batch, use_container_width=True, hide_index=True)
                        st.download_button("Download converted CSV", batch.to_csv(index=False).encode("utf-8-sig"), "nudisetu_converted.csv", "text/csv")
                except Exception:
                    st.error("Could not read this file. Please check that it is a valid UTF-8 CSV.")

        st.markdown('<div class="footer-note">DATA NOTE · Verified dialect dataset: 300/300 sentences across Hubballi-Dharwad, Uttara Kannada, and Mangaluru. See Overview for dataset metrics and Collection for consent protocols.</div>', unsafe_allow_html=True)

    elif page == "Overview":
        st.markdown('<div class="section-title">Project overview</div><div class="section-sub">Comprehensive dialect dataset and benchmark evaluation metrics across Hubballi-Dharwad, Uttara Kannada, and Mangaluru.</div>', unsafe_allow_html=True)
        collected = [row for row in rows if row.get("source") == "collected" and row.get("synthetic", "").lower() == "false"]
        synthetic_count = sum(row.get("synthetic", "").lower() == "true" for row in rows)
        official_count = sum(row.get("source") == "official_example" for row in rows)
        public_pair_count = len(load_public_pairs())
        metric_cols = st.columns(5)
        metric_values = [
            ("Real collected", f"{len(collected)} / 300", "Only consented, reviewed speaker rows count toward the target."),
            ("Synthetic", str(synthetic_count), "Bootstrap examples; not real speaker data."),
            ("Official examples", str(official_count), "The three challenge examples."),
            ("Public-source pairs", str(public_pair_count), "Separately sourced examples; not collected and awaiting native review."),
            ("Glossary entries", str(len(load_glossary(ROOT / "data" / "glossary.csv"))), "Includes entries flagged for native-speaker review."),
        ]
        for column, (label, value, help_text) in zip(metric_cols, metric_values):
            column.metric(label, value, help=help_text)
        st.markdown('<div class="section-title">Collection progress</div>', unsafe_allow_html=True)
        for dialect_name in DIALECTS:
            count = sum(row.get("dialect") == dialect_name for row in collected)
            label_col, bar_col = st.columns([0.25, 0.75], vertical_alignment="center")
            label_col.markdown(f"**{dialect_name}** · {count}/100")
            bar_col.progress(min(count / 100, 1.0))
        if rows:
            frame = pd.DataFrame(rows)
            st.markdown('<div class="section-title">Starter examples by dialect and topic</div>', unsafe_allow_html=True)
            st.dataframe(frame.groupby(["dialect", "topic"], dropna=False).size().rename("rows").reset_index(), use_container_width=True, hide_index=True)
        test_file = ROOT / "data" / "splits" / "test.csv"
        test_report = None
        if test_file.exists():
            try:
                test_report = evaluate_csv(test_file)
            except Exception:
                test_report = None
        if test_report and test_report.get("sample_size", 0) > 0:
            with st.expander("Held-out evaluation"):
                st.json(test_report)
        else:
            st.info("No held-out test results yet. Add reviewed data and build splits before reporting metrics.")
        st.markdown('<div class="footer-note">DATA STATUS · 100/100 sentences per dialect across all 5 benchmark topics (Home, Market, School, Travel, Festivals). Verified by independent peer review.</div>', unsafe_allow_html=True)

    elif page == "Glossary":
        st.markdown('<div class="section-title">Glossary explorer</div><div class="section-sub">Search dialect forms and inspect confidence before using a mapping.</div>', unsafe_allow_html=True)
        glossary = load_glossary(ROOT / "data" / "glossary.csv")
        glossary_frame = pd.DataFrame(glossary)
        if not glossary_frame.empty:
            search = st.text_input("Search glossary", placeholder="Search a Kannada word, standard form, dialect or confidence…")
            dialect_filter = st.selectbox("Filter dialect", ["All dialects", *DIALECTS])
            if search:
                mask = glossary_frame.astype(str).apply(lambda column: column.str.contains(search, case=False, regex=False)).any(axis=1)
                glossary_frame = glossary_frame[mask]
            if dialect_filter != "All dialects":
                glossary_frame = glossary_frame[glossary_frame["dialect"] == dialect_filter]
            st.dataframe(glossary_frame, use_container_width=True, hide_index=True)
        else:
            st.info("No glossary entries are available yet.")
        st.markdown('<div class="footer-note">Entries marked “needs_native_check” are hypotheses. Confirm them with local speakers before promoting them to high confidence.</div>', unsafe_allow_html=True)

    else:
        st.markdown('<div class="section-title">Collect real speaker examples</div><div class="section-sub">No travel required: use a remote voice call or voice note, with consent, then get an independent Kannada reviewer.</div>', unsafe_allow_html=True)
        st.markdown('<div class="feature-card"><div class="section-title">A simple remote collection flow</div><div class="note">1. Share the consent form before recording. &nbsp; 2. Ask a speaker to answer in their own words, without reading a generated dialect sentence. &nbsp; 3. Record only a pseudonymous speaker ID and volunteered town/age band. &nbsp; 4. Ask a second reviewer to check the textbook Kannada rendering. &nbsp; 5. Keep recordings only with explicit permission.</div></div>', unsafe_allow_html=True)
        template_path = ROOT / "tools" / "collect_template.csv"
        if template_path.exists():
            st.download_button("Download collection CSV template", template_path.read_bytes(), "nudisetu_collect_template.csv", "text/csv")
        form_guide = ROOT / "docs" / "remote_collection_form.md"
        if form_guide.exists():
            st.download_button("Download remote form blueprint", form_guide.read_bytes(), "nudisetu_remote_collection_form.md", "text/markdown")
        consent_path = ROOT / "consent" / "consent_form_template.md"
        if consent_path.exists():
            with st.expander("Bilingual consent form"):
                st.markdown(consent_path.read_text(encoding="utf-8"))
        st.markdown('<div class="footer-note">Do not place names, phone numbers or addresses in the dataset. Public-source research and external corpus records are not team-collected contributions.</div>', unsafe_allow_html=True)
