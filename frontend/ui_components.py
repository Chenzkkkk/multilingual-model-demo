from __future__ import annotations

import html
import json
from typing import Any

import matplotlib.pyplot as plt
import streamlit as st


def apply_matplotlib_chinese_style() -> None:
    plt.rcParams["font.sans-serif"] = [
        "Microsoft YaHei",
        "SimHei",
        "Noto Sans CJK SC",
        "PingFang SC",
        "Arial Unicode MS",
        "DejaVu Sans",
    ]
    plt.rcParams["axes.unicode_minus"] = False
    plt.rcParams["figure.facecolor"] = "#f5f7fb"
    plt.rcParams["axes.facecolor"] = "#ffffff"
    plt.rcParams["axes.edgecolor"] = "#d0d8e8"
    plt.rcParams["axes.labelcolor"] = "#1f2a44"
    plt.rcParams["xtick.color"] = "#2f3e5e"
    plt.rcParams["ytick.color"] = "#2f3e5e"
    plt.rcParams["text.color"] = "#1f2a44"
    plt.rcParams["axes.titleweight"] = "bold"
    plt.rcParams["axes.titlesize"] = 12


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
[data-testid="stSidebarNav"] a[href*="stage4_test"],
[data-testid="stSidebarNav"] a[href*="benchmark"] {
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
    transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.info-card:hover {
    transform: translateY(-2px);
    box-shadow: 0 10px 24px rgba(15, 76, 129, 0.08);
}

.result-card {
    background: #ffffff;
    border: 1px solid var(--line);
    border-radius: 14px;
    padding: 1rem 1.1rem;
    margin: 0.8rem 0;
    box-shadow: 0 8px 20px rgba(17, 36, 63, 0.06);
}

.section-banner {
    border: 1px solid var(--line);
    border-radius: 14px;
    padding: 0.8rem 1rem;
    background: linear-gradient(95deg, #ffffff 0%, #edf4ff 100%);
    margin: 0.4rem 0 0.9rem 0;
}

.section-banner h3 {
    margin: 0;
    color: var(--primary);
    font-size: 1.05rem;
}

.section-banner p {
    margin: 0.25rem 0 0 0;
    color: var(--muted);
    font-size: 0.92rem;
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


def render_section_banner(title: str, subtitle: str) -> None:
    st.markdown(
        f"""
<div class="section-banner">
  <h3>{html.escape(title)}</h3>
  <p>{html.escape(subtitle)}</p>
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
                translations = payload.get("translations")
                if isinstance(translations, list) and translations:
                    for item in translations[:8]:
                        if isinstance(item, dict):
                            lang = str(item.get("language") or item.get("language_code") or "未知语言")
                            text = str(item.get("text") or "").strip()
                            if text:
                                output_lines.append(f"{lang}: {text}")

            # 5) 通用文本输出字段
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

            # 6) XLM 跨语言相似度结构
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


def _extract_result_text(payload: Any) -> str:
    if isinstance(payload, str):
        return payload.strip()
    if not isinstance(payload, dict):
        return str(payload or "").strip()

    translations = payload.get("translations")
    if isinstance(translations, list) and translations:
        lines: list[str] = []
        for item in translations:
            if isinstance(item, dict):
                lang = str(item.get("language") or item.get("language_code") or "")
                txt = str(item.get("text") or "").strip()
                if txt:
                    lines.append(f"{lang}: {txt}" if lang else txt)
        if lines:
            return "\n".join(lines)

    for key in ["output", "result", "generated_text", "translated_text", "answer", "text", "response"]:
        value = payload.get(key)
        if isinstance(value, str) and value.strip():
            return value.strip()

    return str(payload).strip()


def render_stage_comparison_charts(results: list[dict[str, Any]], title: str = "横向比较") -> None:
    if not isinstance(results, list) or not results:
        return

    rows: list[dict[str, Any]] = []
    for item in results:
        if not isinstance(item, dict):
            continue
        model_name = str(item.get("model") or "Unknown")
        success = bool(item.get("success", False))
        text = _extract_result_text(item.get("result"))
        rows.append(
            {
                "model": model_name,
                "success": 1 if success else 0,
                "output_len": len(text),
                "line_count": len([line for line in text.splitlines() if line.strip()]),
            }
        )

    if not rows:
        return

    apply_matplotlib_chinese_style()
    st.markdown(f"### {title}")

    model_names = [r["model"] for r in rows]
    success_values = [r["success"] for r in rows]
    output_lens = [r["output_len"] for r in rows]
    line_counts = [r["line_count"] for r in rows]
    palette = ["#154c79", "#1f7a8c", "#bf7f2f", "#b23a48", "#4c6a92", "#7a5195", "#2d936c", "#db7c26"]
    colors = [palette[idx % len(palette)] for idx, _ in enumerate(model_names)]

    fig, axes = plt.subplots(1, 2, figsize=(13.2, 4.8), dpi=120)
    fig.patch.set_facecolor("#f5f7fb")

    bars_left = axes[0].bar(model_names, success_values, color=colors, edgecolor="#e9edf5", linewidth=1.0)
    axes[0].set_title("模型运行状态")
    axes[0].set_ylabel("成功标记")
    axes[0].set_ylim(0, 1.15)
    axes[0].grid(axis="y", linestyle="--", alpha=0.25, linewidth=0.8)
    axes[0].tick_params(axis="x", rotation=24)
    for bar, val in zip(bars_left, success_values):
        axes[0].text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height() + 0.03,
            "成功" if val else "失败",
            ha="center",
            va="bottom",
            fontsize=9,
            color="#2c3b57",
        )

    bars_right = axes[1].bar(model_names, output_lens, color=colors, edgecolor="#e9edf5", linewidth=1.0)
    axes[1].set_title("输出信息密度")
    axes[1].set_ylabel("字符数")
    axes[1].grid(axis="y", linestyle="--", alpha=0.25, linewidth=0.8)
    axes[1].tick_params(axis="x", rotation=24)
    for bar, chars, lines in zip(bars_right, output_lens, line_counts):
        axes[1].text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height() + max(output_lens + [1]) * 0.015,
            f"{chars}字/{lines}行",
            ha="center",
            va="bottom",
            fontsize=8.6,
            color="#2c3b57",
        )

    for ax in axes:
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)

    fig.tight_layout()
    st.pyplot(fig, use_container_width=True)

    st.caption("说明：该图用于课堂横向展示，不代表严格学术指标；建议配合 benchmark 页的任务指标一起看。")


def _render_stage_signature_radar(results: list[dict[str, Any]]) -> None:
    if not results:
        return
    apply_matplotlib_chinese_style()

    success_rate = sum(1 for r in results if r.get("success")) / max(len(results), 1)
    text_lengths = [len(_extract_result_text(r.get("result"))) for r in results]
    avg_len = (sum(text_lengths) / len(text_lengths)) if text_lengths else 0.0
    max_len = max(text_lengths + [1])
    richness = min(avg_len / max_len, 1.0)
    stability = 1.0 - (text_lengths.count(0) / max(len(text_lengths), 1))

    labels = ["稳定性", "信息量", "完成率", "可读性"]
    values = [stability, richness, success_rate, min((success_rate + richness) / 1.6, 1.0)]
    values += values[:1]

    import math

    angles = [n / float(len(labels)) * 2 * math.pi for n in range(len(labels))]
    angles += angles[:1]

    fig = plt.figure(figsize=(5.2, 4.8), dpi=120)
    ax = plt.subplot(111, polar=True)
    ax.plot(angles, values, color="#1f7a8c", linewidth=2)
    ax.fill(angles, values, color="#1f7a8c", alpha=0.18)
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(labels)
    ax.set_yticks([0.25, 0.5, 0.75, 1.0])
    ax.set_yticklabels(["0.25", "0.5", "0.75", "1.0"], color="#6a7893")
    ax.set_title("阶段表现轮廓", pad=14)
    st.pyplot(fig, use_container_width=False)


def render_stage_results_dashboard(results: list[dict[str, Any]], stage_title: str) -> None:
    if not isinstance(results, list) or not results:
        return

    success_cnt = sum(1 for r in results if r.get("success"))
    total_cnt = len(results)
    success_rate = success_cnt / max(total_cnt, 1)
    avg_len = sum(len(_extract_result_text(r.get("result"))) for r in results) / max(total_cnt, 1)

    c1, c2, c3 = st.columns(3)
    c1.metric("模型数", str(total_cnt))
    c2.metric("运行成功", f"{success_cnt}/{total_cnt}")
    c3.metric("平均输出长度", f"{avg_len:.0f} 字")
    st.progress(min(max(success_rate, 0.0), 1.0), text=f"阶段运行完成度：{success_rate * 100:.0f}%")

    report_payload = {
        "stage": stage_title,
        "summary": {
            "total_models": total_cnt,
            "success_models": success_cnt,
            "success_rate": round(success_rate, 4),
            "avg_output_length": round(avg_len, 2),
        },
        "results": results,
    }
    st.download_button(
        "下载阶段结果报告（JSON）",
        data=json.dumps(report_payload, ensure_ascii=False, indent=2),
        file_name=f"{stage_title}_results.json",
        mime="application/json",
        use_container_width=True,
    )

    tab1, tab2, tab3 = st.tabs(["结果卡片", "图表对比", "模型排行"])
    with tab1:
        for result in results:
            render_model_result(result)
    with tab2:
        col_left, col_right = st.columns([1.6, 1.0])
        with col_left:
            render_stage_comparison_charts(results, title=f"{stage_title}模型对比")
        with col_right:
            _render_stage_signature_radar(results)
    with tab3:
        ranked = []
        max_len = max([len(_extract_result_text(r.get("result"))) for r in results] + [1])
        for r in results:
            length_score = len(_extract_result_text(r.get("result"))) / max_len
            score = (0.75 if r.get("success") else 0.0) + 0.25 * length_score
            ranked.append((str(r.get("model", "Unknown")), score, bool(r.get("success"))))
        ranked.sort(key=lambda x: x[1], reverse=True)

        st.markdown("<div class='table-like'>", unsafe_allow_html=True)
        st.markdown("<div class='row'><div class='key'>模型</div><div class='val'>综合得分（演示用）</div></div>", unsafe_allow_html=True)
        for model, score, ok in ranked:
            status = "成功" if ok else "失败"
            st.markdown(
                f"<div class='row'><div class='key'>{html.escape(model)}</div><div class='val'>{score:.3f} | {status}</div></div>",
                unsafe_allow_html=True,
            )
        st.markdown("</div>", unsafe_allow_html=True)


def _render_single_benchmark_chart(report: dict[str, Any]) -> None:
    if not isinstance(report, dict):
        return

    items = report.get("items", []) if isinstance(report.get("items"), list) else []
    if not items:
        return

    apply_matplotlib_chinese_style()
    case_labels = [str(item.get("case_id", f"case_{idx+1}")) for idx, item in enumerate(items)]
    case_scores = [float(item.get("score", 0.0)) for item in items]
    success_num = int(report.get("call_success", 0))
    fail_num = int(report.get("call_failed", 0))

    fig, axes = plt.subplots(1, 2, figsize=(12.8, 4.9), dpi=120)
    fig.patch.set_facecolor("#f5f7fb")

    colors = ["#1f7a8c" if s >= 0.5 else "#b23a48" for s in case_scores]
    bars = axes[0].bar(case_labels, case_scores, color=colors, edgecolor="#e9edf5", linewidth=1.0)
    axes[0].set_title("逐样例得分")
    axes[0].set_ylabel("分数")
    axes[0].set_ylim(0, 1.05)
    axes[0].grid(axis="y", linestyle="--", alpha=0.25)
    axes[0].tick_params(axis="x", rotation=22)
    for bar, val in zip(bars, case_scores):
        axes[0].text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.02, f"{val:.2f}", ha="center", va="bottom", fontsize=8)

    pie_labels = ["调用成功", "调用失败"]
    pie_vals = [max(success_num, 0), max(fail_num, 0)]
    if sum(pie_vals) == 0:
        pie_vals = [1, 0]
    axes[1].pie(
        pie_vals,
        labels=pie_labels,
        autopct="%1.0f%%",
        startangle=90,
        colors=["#154c79", "#b23a48"],
        wedgeprops={"linewidth": 1.2, "edgecolor": "#f5f7fb"},
        textprops={"fontsize": 10},
    )
    axes[1].set_title("调用稳定性")

    for ax in axes:
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)

    fig.tight_layout()
    st.pyplot(fig, use_container_width=True)


def render_stage_benchmark_panel(stage_id: int) -> None:
    from common.benchmark_runner import MODEL_LABELS, run_benchmark

    stage_task_model_options = {
        1: {
            "stage1_mask_filling": ["bert", "mbert"],
            "stage1_word_sense": ["word2vec", "elmo", "transformer"],
        },
        2: {
            "xnli": ["xlm", "xlmr"],
            "xquad": ["xlm", "xlmr"],
            "belebele": ["xlm", "xlmr"],
        },
        3: {
            "flores_200": ["mbart", "mt5", "bloom", "xglm"],
            "xnli": ["mbart", "mt5", "bloom", "xglm"],
            "mgsm": ["mbart", "mt5", "bloom", "xglm"],
        },
        4: {
            "xnli": ["qwen2", "qwen3", "qwen1", "llama4", "aya"],
            "mgsm": ["qwen2", "qwen3", "qwen1", "llama4", "aya"],
            "xquad": ["qwen2", "qwen3", "qwen1", "llama4", "aya"],
            "belebele": ["qwen2", "qwen3", "qwen1", "llama4", "aya"],
            "flores_200": ["nllb", "madlad400", "qwen_mt", "qwen2", "qwen3"],
        },
    }
    task_title = {
        "stage1_mask_filling": "Stage1-Mask - 掩码预测能力",
        "stage1_word_sense": "Stage1-Sense - 词义消歧与语境理解",
        "xnli": "XNLI - 跨语言逻辑推理",
        "mgsm": "MGSM - 多语言数学推理",
        "xquad": "XQuAD - 跨语言问答抽取",
        "belebele": "BELEBELE - 阅读理解",
        "flores_200": "FLORES-200 - 翻译质量",
    }
    task_desc = {
        "stage1_mask_filling": "面向 BERT/mBERT 的 [MASK] 预测，评估词级语义建模能力。",
        "stage1_word_sense": "面向 Word2Vec/ELMo/Transformer 的词义与语境理解演示评测。",
        "xnli": "判断前提和假设是蕴含、矛盾还是中立，重点看跨语言逻辑一致性。",
        "mgsm": "多语言算术应用题，观察模型在数字、单位、步骤上的稳健性。",
        "xquad": "从给定上下文抽取精准答案，衡量信息定位与抽取能力。",
        "belebele": "多语言阅读理解选择题，评估细节理解与推理能力。",
        "flores_200": "高质量机器翻译评测，考察语义保真、术语与句法迁移。",
    }

    task_model_options = stage_task_model_options.get(stage_id, {"xnli": ["qwen2"]})
    tasks = list(task_model_options.keys())
    st.markdown("### Benchmark 测评")
    st.markdown("以下任务可在本阶段用于横向测评：")
    for task in tasks:
        st.markdown(f"- {task_title.get(task, task)}：{task_desc.get(task, '')}")

    tab_single, tab_compare = st.tabs(["单模型评测", "横向对比"])

    with tab_single:
        col1, col2, col3, col4 = st.columns([1.4, 1.3, 1.0, 0.9])
        with col1:
            selected_task = st.selectbox(
                "选择 Benchmark",
                tasks,
                format_func=lambda x: task_title.get(x, x),
                key=f"s{stage_id}_bench_task",
            )
        with col2:
            model_options = task_model_options.get(selected_task, ["qwen2"])
            selected_model = st.selectbox(
                "选择评测模型",
                model_options,
                format_func=lambda x: MODEL_LABELS.get(x, x),
                key=f"s{stage_id}_bench_model",
            )
        with col3:
            selected_lang = st.selectbox(
                "评测语言",
                ["中文", "英文", "波斯语", "阿拉伯语"],
                index=0,
                key=f"s{stage_id}_bench_lang",
            )
        with col4:
            selected_n = st.number_input(
                "样例数",
                min_value=1,
                max_value=12,
                value=4,
                step=1,
                key=f"s{stage_id}_bench_n",
            )

        if st.button("运行 Benchmark 测评", key=f"s{stage_id}_bench_run", use_container_width=True):
            with st.spinner("正在执行 benchmark 评测，请稍候"):
                report = run_benchmark(
                    task_name=selected_task,
                    model_key=selected_model,
                    language=selected_lang,
                    max_cases=int(selected_n),
                )
            st.session_state[f"s{stage_id}_bench_report"] = report

        report = st.session_state.get(f"s{stage_id}_bench_report")
        if report:
            metric_name = report.get("metric_name", "metric")
            metric_value = float(report.get("metric_value", 0.0))
            c1, c2, c3 = st.columns(3)
            with c1:
                st.metric("任务", task_title.get(report.get("task_name", ""), report.get("task_name", "")))
            with c2:
                st.metric("模型", report.get("model_label", report.get("model_key", "")))
            with c3:
                st.metric(metric_name, f"{metric_value:.4f}")

            _render_single_benchmark_chart(report)

            with st.expander("逐样例明细", expanded=False):
                for idx, item in enumerate(report.get("items", []), start=1):
                    st.markdown(
                        f"""
<div class="info-card">
  <h4 style="margin:0 0 0.45rem 0;">{idx}. {item.get('case_id', '')} | {item.get('case_type', '')}</h4>
  <p style="margin:0.2rem 0;"><strong>正确答案</strong>：{item.get('expected', '')}</p>
  <p style="margin:0.2rem 0;"><strong>模型输出</strong>：{item.get('model_output', '')}</p>
  <p style="margin:0.2rem 0;"><strong>评分</strong>：{float(item.get('score', 0.0)):.4f} | <strong>判定</strong>：{'正确' if item.get('is_correct') else '错误'}</p>
</div>
""",
                        unsafe_allow_html=True,
                    )

    with tab_compare:
        cmp_col1, cmp_col2, cmp_col3 = st.columns([1.4, 1.5, 0.9])
        with cmp_col1:
            cmp_task = st.selectbox(
                "对比任务",
                tasks,
                format_func=lambda x: task_title.get(x, x),
                key=f"s{stage_id}_bench_cmp_task",
            )
        with cmp_col2:
            cmp_models = st.multiselect(
                "对比模型",
                options=task_model_options.get(cmp_task, ["qwen2"]),
                default=task_model_options.get(cmp_task, ["qwen2"])[:3],
                format_func=lambda x: MODEL_LABELS.get(x, x),
                key=f"s{stage_id}_bench_cmp_models",
            )
        with cmp_col3:
            cmp_n = st.number_input(
                "样例数",
                min_value=1,
                max_value=12,
                value=4,
                step=1,
                key=f"s{stage_id}_bench_cmp_n",
            )

        cmp_langs = st.multiselect(
            "对比语言",
            options=["中文", "英文", "波斯语", "阿拉伯语"],
            default=["中文", "英文", "波斯语"],
            key=f"s{stage_id}_bench_cmp_langs",
        )

        if st.button("运行横向对比", key=f"s{stage_id}_bench_cmp_run", use_container_width=True):
            if not cmp_models or not cmp_langs:
                st.warning("请至少选择一个模型和一种语言")
            else:
                reports = []
                with st.spinner("正在执行横向对比"):
                    for lang in cmp_langs:
                        for model in cmp_models:
                            rep = run_benchmark(cmp_task, model, lang, int(cmp_n))
                            reports.append(rep)
                st.session_state[f"s{stage_id}_bench_cmp_reports"] = reports

        cmp_reports = st.session_state.get(f"s{stage_id}_bench_cmp_reports", [])
        if cmp_reports:
            apply_matplotlib_chinese_style()
            langs = []
            models = []
            for rep in cmp_reports:
                lang = rep.get("language", "")
                model = rep.get("model_label", rep.get("model_key", ""))
                if lang not in langs:
                    langs.append(lang)
                if model not in models:
                    models.append(model)

            value_map = {(rep.get("model_label", rep.get("model_key", "")), rep.get("language", "")): float(rep.get("metric_value", 0.0)) for rep in cmp_reports}
            matrix = [[value_map.get((m, l), 0.0) for m in models] for l in langs]

            fig, ax = plt.subplots(figsize=(1.2 * max(len(models), 3) + 3, 0.9 * max(len(langs), 3) + 2), dpi=120)
            im = ax.imshow(matrix, cmap="YlGnBu", aspect="auto", vmin=0.0, vmax=1.0)
            ax.set_xticks(list(range(len(models))))
            ax.set_xticklabels(models, rotation=20, ha="right")
            ax.set_yticks(list(range(len(langs))))
            ax.set_yticklabels(langs)
            ax.set_title("模型-语言得分矩阵")
            for i in range(len(langs)):
                for j in range(len(models)):
                    ax.text(j, i, f"{matrix[i][j]:.2f}", ha="center", va="center", color="#0f2f4d", fontsize=8.5)
            fig.colorbar(im, ax=ax, fraction=0.03, pad=0.02)
            fig.tight_layout()
            st.pyplot(fig, use_container_width=True)
