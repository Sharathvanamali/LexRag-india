import streamlit as st
from langchain_ollama.llms import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
from vector import retriever

# ─────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="LexAI — Judicial Intelligence",
    page_icon="⚖️",
    layout="centered"
)

# ─────────────────────────────────────────────
# CUSTOM CSS
# ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;700;900&family=Crimson+Pro:ital,wght@0,300;0,400;1,300&family=JetBrains+Mono:wght@300;400&display=swap');

/* ── ROOT VARIABLES ── */
:root {
    --gold:        #C9A84C;
    --gold-light:  #E8C97A;
    --gold-dim:    #7A6230;
    --obsidian:    #080B12;
    --navy:        #0C1220;
    --panel:       #111827;
    --panel-light: #1A2538;
    --border:      rgba(201,168,76,0.25);
    --text:        #D6C9A8;
    --text-muted:  #6B7280;
    --glow:        rgba(201,168,76,0.15);
}

/* ── GLOBAL RESET ── */
html, body, [data-testid="stAppViewContainer"] {
    background: var(--obsidian) !important;
    color: var(--text) !important;
    font-family: 'Crimson Pro', Georgia, serif !important;
}

[data-testid="stHeader"] { background: transparent !important; }
[data-testid="stSidebar"] { display: none; }
.block-container {
    max-width: 860px !important;
    padding: 0 2rem 6rem !important;
}

/* ── ANIMATED BACKGROUND GRID ── */
[data-testid="stAppViewContainer"]::before {
    content: '';
    position: fixed;
    inset: 0;
    background-image:
        linear-gradient(rgba(201,168,76,0.03) 1px, transparent 1px),
        linear-gradient(90deg, rgba(201,168,76,0.03) 1px, transparent 1px);
    background-size: 48px 48px;
    pointer-events: none;
    z-index: 0;
}

/* ── HEADER SECTION ── */
.lex-header {
    text-align: center;
    padding: 3.5rem 0 2rem;
    position: relative;
}
.lex-emblem {
    font-size: 3.2rem;
    display: block;
    margin-bottom: 0.4rem;
    filter: drop-shadow(0 0 18px rgba(201,168,76,0.6));
    animation: pulse-glow 3s ease-in-out infinite;
}
@keyframes pulse-glow {
    0%, 100% { filter: drop-shadow(0 0 12px rgba(201,168,76,0.5)); }
    50%       { filter: drop-shadow(0 0 28px rgba(201,168,76,0.9)); }
}
.lex-title {
    font-family: 'Playfair Display', serif !important;
    font-size: 2.8rem !important;
    font-weight: 900 !important;
    letter-spacing: 0.06em;
    background: linear-gradient(135deg, var(--gold-light) 0%, var(--gold) 50%, var(--gold-dim) 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin: 0 !important;
    line-height: 1.1 !important;
}
.lex-subtitle {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.72rem;
    letter-spacing: 0.35em;
    color: var(--gold-dim);
    text-transform: uppercase;
    margin-top: 0.5rem;
}
.lex-divider {
    width: 280px;
    height: 1px;
    background: linear-gradient(90deg, transparent, var(--gold), transparent);
    margin: 1.5rem auto;
}
.lex-tagline {
    font-size: 1rem;
    font-style: italic;
    color: var(--text-muted);
    letter-spacing: 0.04em;
}

/* ── STATS BAR ── */
.lex-stats {
    display: flex;
    justify-content: center;
    gap: 2.5rem;
    margin: 1.5rem 0 2.5rem;
    padding: 1rem 2rem;
    background: linear-gradient(135deg, var(--panel) 0%, var(--panel-light) 100%);
    border: 1px solid var(--border);
    border-radius: 4px;
    position: relative;
    overflow: hidden;
}
.lex-stats::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 2px;
    background: linear-gradient(90deg, transparent, var(--gold), transparent);
}
.stat-item { text-align: center; }
.stat-value {
    font-family: 'JetBrains Mono', monospace;
    font-size: 1.4rem;
    color: var(--gold);
    display: block;
}
.stat-label {
    font-size: 0.72rem;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    color: var(--text-muted);
}

/* ── CHAT MESSAGES ── */
[data-testid="stChatMessage"] {
    background: transparent !important;
    border: none !important;
    padding: 0.25rem 0 !important;
}

/* User bubble */
[data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-user"]) .stMarkdown {
    background: linear-gradient(135deg, #1C2A1A 0%, #162415 100%) !important;
    border: 1px solid rgba(100,180,80,0.2) !important;
    border-left: 3px solid #5A9A4A !important;
    border-radius: 2px 8px 8px 2px !important;
    padding: 1rem 1.2rem !important;
    font-size: 1.05rem !important;
    color: #C8DFC4 !important;
}

/* Assistant bubble */
[data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-assistant"]) .stMarkdown {
    background: linear-gradient(135deg, var(--panel) 0%, #151F30 100%) !important;
    border: 1px solid var(--border) !important;
    border-left: 3px solid var(--gold) !important;
    border-radius: 2px 8px 8px 2px !important;
    padding: 1.2rem 1.4rem !important;
    font-size: 1.08rem !important;
    line-height: 1.75 !important;
    color: var(--text) !important;
    box-shadow: 0 4px 24px rgba(0,0,0,0.4), inset 0 0 40px rgba(201,168,76,0.03) !important;
}

/* Avatar icons */
[data-testid="chatAvatarIcon-user"] {
    background: #1C3518 !important;
    border: 1px solid rgba(100,180,80,0.3) !important;
}
[data-testid="chatAvatarIcon-assistant"] {
    background: var(--panel-light) !important;
    border: 1px solid var(--border) !important;
}

/* ── CHAT INPUT ── */
[data-testid="stChatInputContainer"] {
    background: var(--panel) !important;
    border: 1px solid var(--border) !important;
    border-radius: 4px !important;
    padding: 0.2rem 0.5rem !important;
    box-shadow: 0 0 30px rgba(201,168,76,0.08) !important;
}
[data-testid="stChatInputContainer"]::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 1px;
    background: linear-gradient(90deg, transparent, var(--gold), transparent);
}
[data-testid="stChatInput"] textarea {
    background: transparent !important;
    color: var(--text) !important;
    font-family: 'Crimson Pro', serif !important;
    font-size: 1.05rem !important;
    border: none !important;
    caret-color: var(--gold) !important;
}
[data-testid="stChatInput"] textarea::placeholder {
    color: var(--text-muted) !important;
    font-style: italic;
}
[data-testid="stChatInputSubmitButton"] {
    color: var(--gold) !important;
}

/* ── SPINNER ── */
[data-testid="stSpinner"] {
    color: var(--gold) !important;
}
[data-testid="stSpinner"] > div {
    border-top-color: var(--gold) !important;
}

/* ── FOOTER SEAL ── */
.lex-footer {
    text-align: center;
    margin-top: 3rem;
    padding-top: 1.5rem;
    border-top: 1px solid rgba(201,168,76,0.1);
}
.lex-footer-text {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.65rem;
    letter-spacing: 0.22em;
    color: var(--gold-dim);
    text-transform: uppercase;
}

/* ── SCROLLBAR ── */
::-webkit-scrollbar { width: 4px; }
::-webkit-scrollbar-track { background: var(--obsidian); }
::-webkit-scrollbar-thumb { background: var(--gold-dim); border-radius: 2px; }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# HEADER
# ─────────────────────────────────────────────
st.markdown("""
<div class="lex-header">
    <span class="lex-emblem">⚖️</span>
    <h1 class="lex-title">LexAI</h1>
    <p class="lex-subtitle">Judicial Intelligence System &nbsp;·&nbsp; v2.5.0</p>
    <div class="lex-divider"></div>
    <p class="lex-tagline">"Fiat justitia ruat caelum — Let justice be done though the heavens fall."</p>
</div>

<div class="lex-stats">
    <div class="stat-item">
        <span class="stat-value">25+</span>
        <span class="stat-label">Years Precedent</span>
    </div>
    <div class="stat-item">
        <span class="stat-value">⚡</span>
        <span class="stat-label">AI-Augmented</span>
    </div>
    <div class="stat-item">
        <span class="stat-value">RAG</span>
        <span class="stat-label">Retrieval Engine</span>
    </div>
    <div class="stat-item">
        <span class="stat-value">🔒</span>
        <span class="stat-label">Local & Private</span>
    </div>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# LLM & CHAIN  ← UNCHANGED LOGIC
# ─────────────────────────────────────────────
@st.cache_resource
def get_chain():
    model = OllamaLLM(model="gemma3:latest")

    template = """
    You are a helpful assistant that answers questions based on the provided document records.
    You must follow these rules:
    - Use ONLY the provided document records to answer
    - Do NOT make assumptions or add information not present in the records
    - If the answer is not found in the records, say: "The data does not contain this information."

    Document records:
    {records}

    User question:
    {question}
    """

    prompt = ChatPromptTemplate.from_template(template)
    return prompt | model

chain = get_chain()

# ─────────────────────────────────────────────
# CHAT HISTORY  ← UNCHANGED LOGIC
# ─────────────────────────────────────────────
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# ─────────────────────────────────────────────
# USER INPUT  ← UNCHANGED LOGIC
# ─────────────────────────────────────────────
if question := st.chat_input("Submit your legal query to the bench..."):

    with st.chat_message("user"):
        st.markdown(question)

    st.session_state.messages.append({"role": "user", "content": question})

    with st.chat_message("assistant"):
        with st.spinner("Deliberating..."):

            records = retriever.invoke(question)

            formatted_records = "\n\n".join(
                f"Title: {doc.metadata.get('title', 'N/A')}\nDescription: {doc.page_content}"
                for doc in records
            )

            response = chain.invoke({
                "records": formatted_records,
                "question": question
            })

            st.markdown(response)

    st.session_state.messages.append({"role": "assistant", "content": response})

# ─────────────────────────────────────────────
# FOOTER
# ─────────────────────────────────────────────
st.markdown("""
<div class="lex-footer">
    <p class="lex-footer-text">LexAI Judicial Intelligence &nbsp;·&nbsp; Powered by Ollama + LangChain &nbsp;·&nbsp; All deliberations are confidential</p>
</div>
""", unsafe_allow_html=True)