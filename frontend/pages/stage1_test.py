import sys
from pathlib import Path

import streamlit as st

project_root = Path(__file__).resolve().parents[2]
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from common.utils import EXAMPLE_INPUTS
from frontend.ui_components import (
    inject_base_styles,
    render_page_header,
    render_section_banner,
    render_stage_benchmark_panel,
    render_stage_results_dashboard,
)
from stage1.demo import run_demo

inject_base_styles()

render_page_header(
    "第一阶段测试页面",
    "用于运行 Word2Vec, ELMo, Transformer, BERT, mBERT。页面仅展示输入与可读结果。",
)

st.markdown("### 本页测试模型")
st.markdown("Word2Vec, ELMo, Transformer, BERT, mBERT")

render_section_banner("第一部分：通俗测试与结果展示", "用于课堂演示模型直观输出，输入框可随时改写。")

if st.button("返回第一阶段讲解", use_container_width=False):
    st.switch_page("pages/stage1.py")

models_config = {
    "Word2Vec": {
        "input_type": "word",
        "param_name": "word2vec_word",
        "default": "bank",
        "instruction": "输入一个词，查看最相近词。",
        "examples": EXAMPLE_INPUTS.get("word2vec", []),
    },
    "ELMo": {
        "input_type": "dual_sentences",
        "param_names": ["elmo_sent1", "elmo_sent2"],
        "defaults": [
            "I went to the bank to close my account before lunch.",
            "The children had a picnic on the river bank after the storm.",
        ],
        "instruction": "输入两句包含同一词的句子，观察词义差异。",
        "examples": EXAMPLE_INPUTS.get("elmo", []),
    },
    "Transformer": {
        "input_type": "text",
        "param_name": "transformer_input",
        "default": "Despite heavy rain and poor visibility, the rescue team coordinated across three cities and completed evacuation overnight.",
        "instruction": "输入一句话，查看 Transformer 结果。",
        "examples": [{"lang": "English", "text": "Multi-head attention is useful"}],
    },
    "BERT": {
        "input_type": "text_with_mask",
        "param_name": "bert_input",
        "default": "After years of drought, the reservoir is finally [MASK] again.",
        "instruction": "输入包含 [MASK] 的文本。",
        "examples": EXAMPLE_INPUTS.get("bert", []),
    },
    "mBERT": {
        "input_type": "text_with_mask",
        "param_name": "mbert_input",
        "default": "这个计划虽然很[MASK]，但只要协作得当，仍有机会完成。",
        "instruction": "输入包含 [MASK] 的多语言文本。",
        "examples": EXAMPLE_INPUTS.get("mbert", []),
    },
}

user_inputs = {}
for model_name, config in models_config.items():
    with st.expander(f"{model_name} 输入", expanded=False):
        st.caption(config["instruction"])

        if config.get("examples"):
            sample_lines = []
            for ex in config["examples"][:3]:
                if isinstance(ex, dict):
                    sample_lines.append(f"{ex.get('lang', '')}: {ex.get('text', '')}")
            if sample_lines:
                st.text("示例:\n" + "\n".join(sample_lines))

        if config["input_type"] == "word":
            user_inputs[config["param_name"]] = st.text_input("输入", value=config["default"], key="s1_word")
        elif config["input_type"] == "dual_sentences":
            user_inputs[config["param_names"][0]] = st.text_area("句子1", value=config["defaults"][0], height=80, key="s1_elmo_1")
            user_inputs[config["param_names"][1]] = st.text_area("句子2", value=config["defaults"][1], height=80, key="s1_elmo_2")
        else:
            user_inputs[config["param_name"]] = st.text_area("输入", value=config["default"], height=90, key=f"s1_{config['param_name']}")

if st.button("运行第一阶段测试", type="primary", use_container_width=True):
    with st.spinner("正在运行模型"):
        try:
            results = run_demo(user_inputs)
            st.markdown("### 运行结果")
            render_stage_results_dashboard(results, stage_title="stage1")
        except Exception as exc:
            st.error(str(exc))

st.markdown("---")
render_section_banner("第二部分：Benchmark 测评", "选择任务、模型和语言后，直接得到评测图和明细。")
render_stage_benchmark_panel(stage_id=1)
