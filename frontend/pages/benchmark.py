import sys
from pathlib import Path

import matplotlib.pyplot as plt
import streamlit as st

project_root = Path(__file__).resolve().parents[2]
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from common.benchmark_utils import (
    BENCHMARK_OVERVIEW,
    LANGUAGE_DESIGN_EXPLANATION,
    format_belebele_display,
    format_flores_display,
    format_mgsm_display,
    format_xnli_display,
    format_xquad_display,
    get_benchmark_by_id,
    get_default_language,
    get_example_by_language,
    get_multilingual_versions,
    load_benchmarks,
)
from common.benchmark_runner import MODEL_LABELS, TASK_MODEL_OPTIONS, run_benchmark
from frontend.ui_components import apply_matplotlib_chinese_style, inject_base_styles, render_page_header

inject_base_styles()

render_page_header(
    "多语言评测案例库",
    "中文优先展示多语言 benchmark 案例，并支持对模型进行可执行评测。",
)

st.markdown("### 这块是做什么的")
st.markdown(
    """
- 这里是平台的 benchmark 入口，对应 XNLI、MGSM、FLORES、XQuAD、BELEBELE 等官方常用任务。
- 你可以先查看每个任务的标准样例，再直接调用模型跑评测。
- 页面会返回任务级指标和逐样例结果，便于课堂演示、作业验收和模型对比。
"""
)

st.markdown("### 官方测评入口")

benchmarks = load_benchmarks()

task_types = {
    "xnli": "XNLI - 跨语言逻辑推理",
    "mgsm": "MGSM - 数学推理",
    "flores_200": "FLORES - 翻译质量",
    "xquad": "XQuAD - 问答系统",
    "belebele": "BELEBELE - 阅读理解",
}

run_col1, run_col2, run_col3, run_col4 = st.columns([1.5, 1.2, 1.2, 0.9])
with run_col1:
    run_task = st.selectbox("评测任务", list(task_types.keys()), format_func=lambda x: task_types[x], key="bench_run_task")
with run_col2:
    model_options = TASK_MODEL_OPTIONS.get(run_task, ["qwen2"])
    run_model = st.selectbox(
        "评测模型",
        model_options,
        format_func=lambda x: MODEL_LABELS.get(x, x),
        key="bench_run_model",
    )
with run_col3:
    run_language = st.selectbox("评测语言", ["中文", "英文", "波斯语", "阿拉伯语"], index=0, key="bench_run_lang")
with run_col4:
    run_max_cases = st.number_input("样例数", min_value=1, max_value=10, value=3, step=1, key="bench_run_n")

if st.button("运行官方 benchmark 评测", type="primary", use_container_width=True):
    with st.spinner("正在执行 benchmark 评测，请稍候"):
        report = run_benchmark(
            task_name=run_task,
            model_key=run_model,
            language=run_language,
            max_cases=int(run_max_cases),
        )
        st.session_state["benchmark_report"] = report

st.markdown("### 横向比较（多模型 / 多语言）")
cmp_col1, cmp_col2, cmp_col3 = st.columns([1.4, 1.6, 1.0])
with cmp_col1:
    cmp_task = st.selectbox("对比任务", list(task_types.keys()), format_func=lambda x: task_types[x], key="bench_cmp_task")
with cmp_col2:
    cmp_models = st.multiselect(
        "对比模型（可多选）",
        options=TASK_MODEL_OPTIONS.get(cmp_task, ["qwen2"]),
        default=TASK_MODEL_OPTIONS.get(cmp_task, ["qwen2"])[:3],
        format_func=lambda x: MODEL_LABELS.get(x, x),
        key="bench_cmp_models",
    )
with cmp_col3:
    cmp_max_cases = st.number_input("每模型样例数", min_value=1, max_value=12, value=4, step=1, key="bench_cmp_n")

cmp_languages = st.multiselect(
    "对比语言（可多选）",
    options=["中文", "英文", "波斯语", "阿拉伯语"],
    default=["中文", "英文", "波斯语"],
    key="bench_cmp_langs",
)

if st.button("运行横向比较", use_container_width=True):
    if not cmp_models:
        st.warning("请至少选择一个模型")
    elif not cmp_languages:
        st.warning("请至少选择一种语言")
    else:
        all_reports = []
        with st.spinner("正在执行横向比较，请稍候"):
            for lang in cmp_languages:
                for model in cmp_models:
                    rep = run_benchmark(
                        task_name=cmp_task,
                        model_key=model,
                        language=lang,
                        max_cases=int(cmp_max_cases),
                    )
                    all_reports.append(rep)
        st.session_state["benchmark_compare_reports"] = all_reports

cmp_reports = st.session_state.get("benchmark_compare_reports", [])
if cmp_reports:
    st.markdown("#### 横向比较结果图")
    metric_name = cmp_reports[0].get("metric_name", "metric")
    apply_matplotlib_chinese_style()

    languages = []
    models = []
    for rep in cmp_reports:
        lang = rep.get("language", "")
        model = rep.get("model_label", rep.get("model_key", ""))
        if lang not in languages:
            languages.append(lang)
        if model not in models:
            models.append(model)

    score_map = {(rep.get("model_label", rep.get("model_key", "")), rep.get("language", "")): float(rep.get("metric_value", 0.0)) for rep in cmp_reports}

    fig, ax = plt.subplots(figsize=(12.8, 5.4), dpi=120)
    palette = ["#154c79", "#1f7a8c", "#bf7f2f", "#b23a48", "#4c6a92", "#7a5195"]
    n = len(models)
    total_width = 0.8
    bar_width = total_width / max(n, 1)
    x = list(range(len(languages)))

    for idx, model in enumerate(models):
        vals = [score_map.get((model, lang), 0.0) for lang in languages]
        pos = [xx - total_width / 2 + idx * bar_width + bar_width / 2 for xx in x]
        bars = ax.bar(pos, vals, width=bar_width * 0.92, label=model, color=palette[idx % len(palette)], edgecolor="#e9edf5", linewidth=1.0)
        for bar, val in zip(bars, vals):
            ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.008, f"{val:.2f}", ha="center", va="bottom", fontsize=8)

    ax.set_xticks(x)
    ax.set_xticklabels(languages)
    ax.set_title(f"多模型多语言横向比较（{metric_name}）")
    ax.set_ylabel(metric_name)
    ax.grid(axis="y", linestyle="--", alpha=0.25)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.14), ncol=2, frameon=False)
    fig.tight_layout()

    st.pyplot(fig, use_container_width=True)

    st.markdown("#### 对比明细")
    for rep in cmp_reports:
        st.markdown(
            f"- 任务: {task_types.get(rep.get('task_name', ''), rep.get('task_name', ''))} | 模型: {rep.get('model_label', rep.get('model_key', ''))} | 语言: {rep.get('language', '')} | {rep.get('metric_name', 'metric')}: {float(rep.get('metric_value', 0.0)):.4f} | 成功调用: {rep.get('call_success', 0)} / {rep.get('num_cases', 0)}"
        )

report = st.session_state.get("benchmark_report")
if report:
    st.markdown("#### 评测结果总览")
    metric_name = report.get("metric_name", "metric")
    metric_value = float(report.get("metric_value", 0.0))
    c1, c2, c3 = st.columns(3)
    with c1:
        st.metric("任务", task_types.get(report.get("task_name", ""), report.get("task_name", "")))
    with c2:
        st.metric("模型", report.get("model_label", report.get("model_key", "")))
    with c3:
        st.metric(metric_name, f"{metric_value:.4f}")

    st.caption(
        f"样例数: {report.get('num_cases', 0)} | 成功调用: {report.get('call_success', 0)} | 调用失败: {report.get('call_failed', 0)}"
    )

    st.markdown("#### 逐样例结果")
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

with st.expander("语言设计说明", expanded=False):
    st.markdown(LANGUAGE_DESIGN_EXPLANATION)

selected_task = st.sidebar.radio(
    "任务",
    list(task_types.keys()),
    format_func=lambda x: task_types[x],
)

st.sidebar.markdown("---")
with st.sidebar.expander("任务说明", expanded=False):
    st.markdown(BENCHMARK_OVERVIEW)

st.markdown(f"### {task_types[selected_task]}")

if selected_task in benchmarks:
    task_data = benchmarks[selected_task]

    if isinstance(task_data, list) and task_data:
        case_ids = [item.get("id", f"case_{i}") for i, item in enumerate(task_data)]
        case_names = [f"案例 {i + 1}: {item.get('type', '未知')}" for i, item in enumerate(task_data)]
        tabs = st.tabs(case_names)

        for tab, case_id in zip(tabs, case_ids):
            with tab:
                case_data = get_benchmark_by_id(selected_task, case_id)
                if not case_data:
                    st.warning("未找到该案例数据")
                    continue

                st.markdown(f"#### {case_data.get('type', '未知类型')}")

                languages = get_multilingual_versions(case_data)
                default_lang = get_default_language(case_data)

                sorted_languages = []
                if "中文" in languages:
                    sorted_languages.append("中文")
                sorted_languages.extend([lang for lang in languages if lang != "中文"])

                default_idx = 0
                if default_lang in sorted_languages:
                    default_idx = sorted_languages.index(default_lang)

                selected_lang = st.radio(
                    "选择语言",
                    sorted_languages,
                    index=default_idx,
                    horizontal=True,
                    key=f"lang_{selected_task}_{case_id}",
                )

                example = get_example_by_language(case_data, selected_lang)
                if not example:
                    st.warning("该语言暂无示例")
                    continue

                if selected_task == "xnli":
                    content = format_xnli_display(example)
                elif selected_task == "mgsm":
                    content = format_mgsm_display(example)
                elif selected_task == "flores_200":
                    content = format_flores_display(example)
                elif selected_task == "xquad":
                    content = format_xquad_display(example)
                else:
                    content = format_belebele_display(example)

                st.markdown(content)

                if selected_lang == "中文":
                    st.info("建议先阅读中文版本理解任务，再切换到其他语言观察差异。")

with st.expander("课堂演示建议", expanded=False):
    st.markdown(
        """
1. 先用中文版本确认题意与标准答案。
2. 切换到其他语言，对比同一道题的表达形式。
3. 将题目输入对应模型，比较输出质量。
4. 归纳不同语言、不同任务上的稳定性差异。
5. 在“横向比较”模块同时勾选多个模型和语言，得到一张可课堂展示的对比图。
"""
    )
