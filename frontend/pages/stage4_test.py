import sys
from pathlib import Path

import streamlit as st

project_root = Path(__file__).resolve().parents[2]
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from common.benchmark_utils import load_benchmarks
from frontend.ui_components import inject_base_styles, render_model_result, render_page_header
from stage4.demo import run_demo

inject_base_styles()

render_page_header(
    "第四阶段测试页面",
    "用于运行 Qwen1, Qwen2, Qwen3, Qwen-MT, LLaMA4, NLLB, MADLAD-400, Aya。",
)

st.markdown("### 本页测试模型")
st.markdown("Qwen1, Qwen2, Qwen3, Qwen-MT, LLaMA4, NLLB, MADLAD-400, Aya")

if st.button("返回第四阶段讲解", use_container_width=False):
    st.switch_page("pages/stage4.py")

benchmarks = load_benchmarks()
flores_cases = benchmarks.get("flores_200", [])
hard_case_options = []
for item in flores_cases:
    item_id = item.get("id", "")
    case_type = item.get("type", "")
    examples = item.get("examples", [])
    if examples:
        src = examples[0].get("source", "")
        hard_case_options.append((f"{item_id} | {case_type}", src))

with st.expander("翻译测试样例", expanded=False):
    if hard_case_options:
        labels = [x[0] for x in hard_case_options]
        selected = st.selectbox("选择案例", labels, index=0)
        selected_src = dict(hard_case_options).get(selected, "")
        if st.button("填入 NLLB 与 MADLAD 输入", key="fill_case"):
            st.session_state["s4_nllb"] = f"translate Chinese to English: {selected_src}"
            st.session_state["s4_madlad"] = f"translate Chinese to English: {selected_src}"
            st.success("已写入输入框")

user_inputs = {}

st.markdown("### Qwen 系列")
for model in ["qwen1", "qwen2", "qwen3"]:
    with st.expander(f"{model.upper()} 输入", expanded=False):
        user_inputs[f"{model}_input"] = st.text_area(
            "输入",
            value="",
            placeholder="请输入你的问题或指令",
            height=90,
            key=f"s4_{model}",
        )

with st.expander("QWEN_MT 输入", expanded=False):
    user_inputs["qwen_mt_input"] = st.text_area(
        "待翻译原文",
        value="",
        placeholder="请输入需要翻译的句子或段落",
        height=100,
        key="s4_qwen_mt_input",
    )
    lang_options = ["Chinese", "English", "Japanese", "Korean", "French", "German", "Spanish", "Arabic", "Russian"]
    c1, c2 = st.columns(2)
    with c1:
        user_inputs["qwen_mt_source_lang"] = st.selectbox("源语言", options=lang_options, index=0, key="s4_qwen_mt_src")
    with c2:
        user_inputs["qwen_mt_target_lang"] = st.selectbox("目标语言", options=lang_options, index=1, key="s4_qwen_mt_tgt")
    user_inputs["qwen_mt_domains"] = st.text_area("领域说明", value="General", height=90, key="s4_qwen_mt_domains")

st.markdown("### 其他模型")
user_inputs["llama4_input"] = st.text_area("LLaMA4 输入", value="What is the future of AI?", height=80, key="s4_llama4")
user_inputs["nllb_input"] = st.text_area(
    "NLLB 输入",
    value=st.session_state.get("s4_nllb", "translate English to Chinese: Hello world"),
    height=80,
    key="s4_nllb",
)
user_inputs["madlad400_input"] = st.text_area(
    "MADLAD-400 输入",
    value=st.session_state.get("s4_madlad", "translate English to Chinese: Hello world"),
    height=80,
    key="s4_madlad",
)
user_inputs["aya_input"] = st.text_area("Aya 输入", value="How can I learn machine learning?", height=80, key="s4_aya")

if st.button("运行第四阶段测试", type="primary", use_container_width=True):
    with st.spinner("正在运行模型"):
        try:
            results = run_demo(user_inputs)
            st.markdown("### 运行结果")
            for result in results:
                render_model_result(result)
        except Exception as exc:
            st.error(str(exc))
