from __future__ import annotations

import html
from typing import Any

import streamlit as st


def inject_base_styles() -> None:
    st.markdown(
        """
<style>
:root {
    --bg-1: #eef5ff;
    --bg-2: #f8fbff;
    --card: #ffffff;
    --line: #cddcf2;
    --text: #10233d;
    --muted: #5b6472;
    --primary: #1559b7;
    --ok: #1e7f4f;
    --err: #b42318;
}

@media (prefers-color-scheme: dark) {
    :root {
        --bg-1: #09080f;
        --bg-2: #140f22;
        --card: #141126;
        --line: #34265b;
        --text: #ece8ff;
        --muted: #beb6dd;
        --primary: #a78bfa;
        --ok: #6ee7b7;
        --err: #fca5a5;
    }
}

html, body, [class*="css"] {
    font-family: "Noto Sans SC", "Microsoft YaHei", "PingFang SC", sans-serif;
    color: var(--text);
}
[data-testid="stSidebarNav"] {
    padding-top: 0.8rem;
}

[data-testid="stSidebarNav"] span {
    font-size: 1.03rem !important;
    font-weight: 600 !important;
}

[data-testid="stSidebarNav"] a {
    border-radius: 10px;
    margin-bottom: 0.16rem;
}

[data-testid="stSidebarNav"] a:hover {
    background: rgba(21, 89, 183, 0.08);
}

[data-testid="stSidebarNav"] a[href*="stage1_test"],
[data-testid="stSidebarNav"] a[href*="stage2_test"],
[data-testid="stSidebarNav"] a[href*="stage3_test"],
[data-testid="stSidebarNav"] a[href*="stage4_test"] {
    display: none !important;
}

[data-testid="stAppViewContainer"] {
    background: linear-gradient(180deg, var(--bg-1) 0%, var(--bg-2) 100%);
}

.page-hero {
    background: linear-gradient(125deg, #ffffff 0%, #e7f1ff 100%);
    border: 1px solid var(--line);
    border-radius: 16px;
    padding: 1.2rem 1.3rem;
    margin-bottom: 1rem;
}

@media (prefers-color-scheme: dark) {
    .page-hero {
        background: linear-gradient(125deg, #17112c 0%, #24183f 100%);
    }
}

.page-title {
    color: var(--primary);
    font-weight: 800;
    font-size: 1.55rem;
    margin: 0 0 0.4rem 0;
}

.page-subtitle {
    color: var(--muted);
    margin: 0;
    line-height: 1.6;
}

.info-card {
    background: var(--card);
    border: 1px solid var(--line);
    border-radius: 14px;
    padding: 1rem 1.1rem;
    margin-bottom: 0.8rem;
}

.result-card {
    background: #ffffff;
    border: 1px solid var(--line);
    border-radius: 14px;
    padding: 1rem 1.1rem;
    margin: 0.8rem 0;
}

.result-title {
    font-size: 1.04rem;
    font-weight: 700;
    color: var(--primary);
    margin-bottom: 0.45rem;
}

.result-kv {
    color: var(--muted);
    font-size: 0.92rem;
    margin-bottom: 0.2rem;
}

.result-input {
    background: #f3f7fc;
    border: 1px solid #dce5f0;
    border-radius: 10px;
    padding: 0.7rem;
    margin-top: 0.55rem;
    white-space: pre-wrap;
}

.result-output {
    background: #eef6ff;
    border: 1px solid #d3e4ff;
    border-radius: 10px;
    padding: 0.7rem;
    margin-top: 0.55rem;
    white-space: pre-wrap;
}

@media (prefers-color-scheme: dark) {
    .result-input {
        background: #171a2c;
        border-color: #2a3460;
    }

    .result-output {
        background: #19152a;
        border-color: #3d2f6d;
    }
}

.result-error {
    background: #fff4f2;
    border: 1px solid #f2d6d2;
    border-radius: 10px;
    padding: 0.7rem;
    margin-top: 0.55rem;
    color: var(--err);
    white-space: pre-wrap;
}

.table-like {
    border: 1px solid var(--line);
    border-radius: 10px;
    overflow: hidden;
}

.table-like .row {
    display: grid;
    grid-template-columns: 180px 1fr;
    border-bottom: 1px solid var(--line);
}

.table-like .row:last-child {
    border-bottom: 0;
}

.table-like .key {
    background: #f6f8fb;
    padding: 0.55rem 0.7rem;
    color: #344054;
    font-weight: 600;
}

.table-like .val {
    background: #ffffff;
    padding: 0.55rem 0.7rem;
    color: #475467;
    white-space: pre-wrap;
}
</style>
""",
        unsafe_allow_html=True,
    )


def render_page_header(title: str, subtitle: str) -> None:
    st.markdown(
        f"""
<div class="page-hero">
  <div class="page-title">{html.escape(title)}</div>
  <p class="page-subtitle">{html.escape(subtitle)}</p>
</div>
""",
        unsafe_allow_html=True,
    )


def _render_simple_table(data: dict[str, Any], preferred_keys: list[str]) -> None:
    rows = []
    used = set()
    for key in preferred_keys:
        if key in data and data.get(key) not in (None, "", [], {}):
            rows.append((key, data.get(key)))
            used.add(key)

    for key, val in data.items():
        if key in used:
            continue
        if isinstance(val, (dict, list)):
            continue
        if val in (None, "", [], {}):
            continue
        rows.append((key, val))

    if not rows:
        return

    st.markdown("<div class='table-like'>", unsafe_allow_html=True)
    for key, val in rows:
        st.markdown(
            f"<div class='row'><div class='key'>{html.escape(str(key))}</div><div class='val'>{html.escape(str(val))}</div></div>",
            unsafe_allow_html=True,
        )
    st.markdown("</div>", unsafe_allow_html=True)


def render_model_result(result: dict[str, Any]) -> None:
    model_name = str(result.get("model", "Unknown Model"))
    success = bool(result.get("success", False))
    payload = result.get("result")
    
    user_input = result.get("user_input") or result.get("input") or result.get("text")
    if isinstance(payload, dict):
        base_input = payload.get("user_input") or payload.get("input") or payload.get("text")
        if base_input and not user_input:
            user_input = base_input

    st.markdown("<div class='result-card'>", unsafe_allow_html=True)
    status = "成功" if success else "失败"
    st.markdown(f"<div class='result-title'>{html.escape(model_name)} | 运行{status}</div>", unsafe_allow_html=True)

    if user_input:
        st.markdown("<div class='result-kv'>输入</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='result-input'>{html.escape(str(user_input))}</div>", unsafe_allow_html=True)

    if success:
        output_lines: list[str] = []

        if isinstance(payload, dict):
            # 1) 最常见的 MLM 预测结构
            predictions = payload.get("predictions")
            if isinstance(predictions, list) and predictions:
                for idx, item in enumerate(predictions[:5], start=1):
                    if isinstance(item, dict):
                        token = item.get("token") or item.get("label") or item.get("word") or ""
                        score = item.get("score")
                        if score is not None:
                            output_lines.append(f"{idx}. {token}（置信度: {score:.4f}）")
                        else:
                            output_lines.append(f"{idx}. {token}")

            # 2) Word2Vec 相近词结构
            if not output_lines:
                results_obj = payload.get("results")
                if isinstance(results_obj, dict):
                    embeds = results_obj.get("embeddings")
                    if isinstance(embeds, list) and embeds:
                        for idx, item in enumerate(embeds[:5], start=1):
                            if isinstance(item, dict):
                                word = item.get("word", "")
                                sim = item.get("similarity_score")
                                if sim is not None:
                                    output_lines.append(f"{idx}. {word}（相似度: {sim:.4f}）")
                                else:
                                    output_lines.append(f"{idx}. {word}")

            # 3) ELMo 示例结构
            if not output_lines:
                demo_obj = payload.get("example_demonstration")
                if isinstance(demo_obj, dict):
                    s1 = demo_obj.get("sentence_1_meaning")
                    s2 = demo_obj.get("sentence_2_meaning")
                    sim_desc = demo_obj.get("embedding_similarity")
                    if s1:
                        output_lines.append(f"句子1词义: {s1}")
                    if s2:
                        output_lines.append(f"句子2词义: {s2}")
                    if sim_desc:
                        output_lines.append(str(sim_desc))

            # 4) 通用文本输出字段
            if not output_lines:
                scalar_keys = [
                    "output",
                    "result",
                    "prediction",
                    "generated_text",
                    "translated_text",
                    "summary",
                    "answer",
                    "attention_explanation",
                    "response",
                    "text",
                ]
                for key in scalar_keys:
                    value = payload.get(key)
                    if isinstance(value, str) and value.strip():
                        output_lines.append(value.strip())
                        break
                    if isinstance(value, list) and value and all(isinstance(x, str) for x in value[:3]):
                        output_lines.extend(value[:5])
                        break

            # 5) XLM 跨语言相似度结构
            if not output_lines:
                score = payload.get("similarity_score")
                text1 = payload.get("text1")
                text2 = payload.get("text2")
                if score is not None:
                    output_lines.append(f"跨语言语义相似度: {score}")
                    if text1:
                        output_lines.append(f"文本1: {text1}")
                    if text2:
                        output_lines.append(f"文本2: {text2}")

            cache_dir = payload.get("cache_dir") if isinstance(payload, dict) else None
            if cache_dir:
                output_lines.append("模型已启用本地缓存，二次运行会更快。")

        elif isinstance(payload, list):
            for item in payload[:5]:
                output_lines.append(str(item))
        elif payload not in (None, ""):
            output_lines.append(str(payload))

        st.markdown("<div class='result-kv'>结果</div>", unsafe_allow_html=True)
        if output_lines:
            st.markdown(
                f"<div class='result-output'>{html.escape(chr(10).join(output_lines))}</div>",
                unsafe_allow_html=True,
            )
        else:
            st.markdown("<div class='result-output'>运行成功，暂无可展示文本结果。</div>", unsafe_allow_html=True)
    else:
        err = payload if isinstance(payload, str) else str(payload)
        st.markdown("<div class='result-kv'>错误信息</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='result-error'>{html.escape(err)}</div>", unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)
