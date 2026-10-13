"""Presentational components. All HTML lives here; app.py stays readable.
Look and feel is identical to the Session 4 demo."""

import streamlit as st


def section_label(text: str):
    st.markdown(f'<span class="section-label">{text}</span>', unsafe_allow_html=True)


def divider():
    st.markdown('<hr class="custom-divider">', unsafe_allow_html=True)


def hero():
    st.markdown("""
    <div style="text-align:center; padding:2.5rem 1rem 1.5rem;">
        <div style="display:inline-block; background:#0D1320; border:1px solid #253450;
                    border-radius:30px; padding:6px 20px; margin-bottom:1.2rem;">
            <span style="font-family:'Space Mono',monospace; font-size:11px;
                         letter-spacing:3px; color:#00D4AA; text-transform:uppercase;">
                🔍 Retrieval Augmented Generation
            </span>
        </div>
        <div class="hero-title">RAG AI Assistant</div>
        <div class="hero-sub">Index any source — Web · PDF · PostgreSQL · Text — then ask AI anything</div>
        <div style="display:inline-block; background:#0D1320; border:1px solid #253450;
                    border-radius:40px; padding:10px 28px;">
            <span style="font-family:'Space Mono',monospace; font-size:12px;
                         color:#6A7A96; letter-spacing:1px;">Built by &nbsp;</span>
            <span style="font-family:'Space Mono',monospace; font-size:14px; font-weight:700;
                         color:#00D4AA; letter-spacing:1px;">Abhinav Rawat</span>
            <span style="font-family:'Space Mono',monospace; font-size:12px;
                         color:#6A7A96; letter-spacing:1px;">&nbsp;·&nbsp;AI Playground</span>
        </div>
    </div>
    """, unsafe_allow_html=True)


def stats_row(n_sources: int, n_chunks: int, model: str):
    st.markdown(f"""
    <div class="stats-row">
        <div class="stat-card">
            <div class="stat-value">{n_sources}</div>
            <div class="stat-label">Sources Indexed</div>
        </div>
        <div class="stat-card">
            <div class="stat-value">{n_chunks}</div>
            <div class="stat-label">Text Chunks</div>
        </div>
        <div class="stat-card">
            <div class="stat-value">{model}</div>
            <div class="stat-label">Model</div>
        </div>
        <div class="stat-card">
            <div class="stat-value" style="color:#4ADE80;">✓</div>
            <div class="stat-label">Ready</div>
        </div>
    </div>
    """, unsafe_allow_html=True)


def source_badge(icon: str, src: str):
    st.markdown(f'<div class="url-card">{icon} {src}</div>', unsafe_allow_html=True)


def chat_turn(turn: int, q: str, a: str):
    st.markdown(f"""
    <div style="background:#0D1320;border:1px solid #253450;border-left:3px solid #8B7FFF;
                border-radius:0 10px 10px 0;padding:10px 14px;margin:6px 0 3px;">
        <span style="font-family:'Space Mono',monospace;font-size:10px;
                     color:#8B7FFF;letter-spacing:2px;">Q{turn}</span>
        <p style="margin:5px 0 0;font-size:15px;color:#F0F2FF;line-height:1.5;">{q}</p>
    </div>
    <div class="answer-card" style="margin-top:3px;">
        <span style="font-family:'Space Mono',monospace;font-size:10px;
                     color:#00D4AA;letter-spacing:2px;">A{turn}</span>
        <p style="margin:5px 0 0;">{a}</p>
    </div>
    """, unsafe_allow_html=True)


def answer_card(answer: str):
    st.markdown(f'<div class="answer-card">{answer}</div>', unsafe_allow_html=True)


def source_chunk_cards(docs, limit: int = 3):
    for i, doc in enumerate(docs[:limit], 1):
        source = doc.metadata.get("source", "Unknown")
        snippet = doc.page_content[:220].replace("\n", " ") + "..."
        st.markdown(f"""
        <div class="source-card">
            <div class="source-url">📄 Chunk {i} — {source}</div>
            {snippet}
        </div>
        """, unsafe_allow_html=True)


def guardrails_sidebar_panel(limiter, metrics):
    """Live Gate 4 budget + observability snapshot. On screen the whole demo."""
    st.markdown('<hr style="border-color:#253450;margin:1.2rem 0;">', unsafe_allow_html=True)
    section_label("🛡 Guardrails")
    st.markdown(f"""
    <div style="font-size:13px;color:#A8B4CC;line-height:1.9;">
        Gate 4 — session budget<br>
        <b style="color:#00D4AA;">{limiter.tokens_used:,}</b>
        <span style="color:#6A7A96;">/ {limiter.max_tokens:,} tokens</span><br>
        <b style="color:#00D4AA;">{limiter.calls_made}</b>
        <span style="color:#6A7A96;">/ {limiter.max_calls} LLM calls</span>
    </div>
    """, unsafe_allow_html=True)
    section_label("📈 Observability")
    st.markdown(f"""
    <div style="font-size:13px;color:#A8B4CC;line-height:1.9;">
        Queries answered: <b style="color:#00D4AA;">{metrics.queries}</b><br>
        Attacks blocked: <b style="color:#FF6B6B;">{metrics.blocked}</b><br>
        Avg latency: <b style="color:#00D4AA;">{metrics.avg_latency_ms:,.0f} ms</b><br>
        <span style="color:#6A7A96;">Trails → </span>
        <span style="font-family:'Space Mono',monospace;color:#8B7FFF;">logs/audit_log.jsonl</span>
    </div>
    """, unsafe_allow_html=True)


def how_it_works():
    st.markdown('<hr style="border-color:#253450;margin:1.2rem 0;">', unsafe_allow_html=True)
    st.markdown("""
    <div style="font-size:13px;color:#6A7A96;line-height:1.9;">
        <b style="color:#A8B4CC;font-size:14px;">How RAG works:</b><br>
        1. Load content from source<br>
        2. Split into 1000-char chunks<br>
        3. Embed chunks → ChromaDB<br>
        4. Your question is embedded<br>
        5. Top 6 similar chunks retrieved<br>
        6. LLM answers from those chunks
    </div>
    """, unsafe_allow_html=True)


def empty_state():
    st.markdown("""
    <div style="background:#0D1320;border:1.5px dashed #253450;border-radius:14px;
                padding:3rem 2rem;text-align:center;margin-top:1rem;">
        <div style="font-size:3.5rem;margin-bottom:1rem;opacity:0.35;">🔍</div>
        <p style="font-family:'Space Mono',monospace;font-size:13px;font-weight:700;
                  color:#6A7A96;letter-spacing:2px;text-transform:uppercase;margin:0 0 10px;">
            No knowledge base loaded
        </p>
        <p style="font-size:15px;color:#3A4A60;line-height:1.75;margin:0;">
            Pick a tab in the sidebar —
            <span style="color:#8B7FFF;">URL</span> ·
            <span style="color:#F5A623;">PDF</span> ·
            <span style="color:#4ADE80;">PostgreSQL</span> ·
            <span style="color:#00D4AA;">Text</span><br>
            Fill in the details and click <b style="color:#00D4AA;">Load & Index</b>
        </p>
    </div>
    """, unsafe_allow_html=True)
