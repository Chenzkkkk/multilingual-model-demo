import sys
from pathlib import Path

import streamlit as st

project_root = Path(__file__).resolve().parents[2]
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from frontend.ui_components import (
    inject_base_styles,
    render_page_header,
    render_section_banner,
    render_stage_benchmark_panel,
    render_stage_results_dashboard,
)
from stage4.demo import run_demo

inject_base_styles()

render_page_header(
    "第四阶段测试页面",
    "用于运行 Qwen1, Qwen2, Qwen3, Qwen-MT, LLaMA4, NLLB, MADLAD-400, Aya。",
)

st.markdown("### 本页测试模型")
st.markdown("Qwen1, Qwen2, Qwen3, Qwen-MT, LLaMA4, NLLB, MADLAD-400, Aya")

render_section_banner("第一部分：通俗测试与结果展示", "统一入口测试 Qwen、LLaMA4、NLLB、MADLAD、Aya 等模型。")

if st.button("返回第四阶段讲解", use_container_width=False):
    st.switch_page("pages/stage4.py")

user_inputs = {}

language_key_to_zh = {
    "chinese": "中文",
    "english": "英语",
    "persian": "波斯语",
    "french": "法语",
    "arabic": "阿拉伯语",
    "hindi": "印地语",
    "spanish": "西班牙语",
    "russian": "俄语",
    "german": "德语",
    "japanese": "日语",
    "korean": "韩语",
}
language_keys = list(language_key_to_zh.keys())

with st.expander("各模型可选语言（中文说明）", expanded=False):
    st.markdown("- Qwen1 / Qwen2 / Qwen3 / LLaMA4 / Aya：用于控制回答语言（可多选）。")
    st.markdown("- Qwen-MT / NLLB / MADLAD-400：用于控制翻译目标语言（可多选）。")
    st.markdown("- 当前可选语言：" + "、".join(language_key_to_zh[k] for k in language_keys))

st.markdown("### Qwen 系列")
for model in ["qwen1", "qwen2", "qwen3"]:
    with st.expander(f"{model.upper()} 输入", expanded=False):
        user_inputs[f"{model}_input"] = st.text_area(
            "输入",
            value={
                "qwen1": "请比较中文、波斯语、阿拉伯语在命名实体翻译时最常见的三个错误，并给出规避策略。",
                "qwen2": "请站在模型评测工程师视角，设计一个多语言鲁棒性测试清单（至少8项）。",
                "qwen3": "给出一个‘看似翻译正确但事实错位’的例子，并解释为什么危险。",
            }[model],
            placeholder="请输入你的问题或指令",
            height=90,
            key=f"s4_{model}",
        )
        user_inputs[f"{model}_langs"] = st.multiselect(
            "回答语言（可多选）",
            options=language_keys,
            default=["chinese"],
            format_func=lambda x: language_key_to_zh.get(x, x),
            key=f"s4_{model}_langs",
            help="若选择多个语言，模型会按选择顺序尽量分别给出回答。",
        )

with st.expander("QWEN_MT 输入", expanded=False):
    user_inputs["qwen_mt_input"] = st.text_area(
        "待翻译原文",
        value="去年获奖的那位科学家回到了她曾经就读的那所大学，并宣布设立青年研究基金。",
        placeholder="请输入需要翻译的句子或段落",
        height=100,
        key="s4_qwen_mt_input",
    )
    qwen_mt_lang_keys = ["chinese", "english", "japanese", "korean", "french", "german", "spanish", "arabic", "russian"]
    c1, c2 = st.columns(2)
    with c1:
        user_inputs["qwen_mt_source_lang"] = st.selectbox(
            "源语言",
            options=qwen_mt_lang_keys,
            index=0,
            format_func=lambda x: language_key_to_zh.get(x, x),
            key="s4_qwen_mt_src",
        )
    with c2:
        user_inputs["qwen_mt_target_langs"] = st.multiselect(
            "目标语言（可多选）",
            options=qwen_mt_lang_keys,
            default=["english"],
            format_func=lambda x: language_key_to_zh.get(x, x),
            key="s4_qwen_mt_tgts",
        )
    user_inputs["qwen_mt_domains"] = st.text_area("领域说明", value="General", height=90, key="s4_qwen_mt_domains")

st.markdown("### 其他模型")
user_inputs["llama4_input"] = st.text_area(
    "LLaMA4 输入",
    value="If a multilingual model performs well in English but poorly in Persian, how would you diagnose the root cause?",
    height=80,
    key="s4_llama4",
)
user_inputs["llama4_langs"] = st.multiselect(
    "LLaMA4 回答语言（可多选）",
    options=language_keys,
    default=["chinese"],
    format_func=lambda x: language_key_to_zh.get(x, x),
    key="s4_llama4_langs",
)
user_inputs["nllb_input"] = st.text_area(
    "NLLB 输入",
    value="这家公司在2024年售出了12540件产品，其中40%来自海外市场。",
    height=80,
    key="s4_nllb",
)
nllb_target_options = ["english", "persian", "french", "arabic", "hindi", "spanish", "russian", "german"]
user_inputs["nllb_target_langs"] = st.multiselect(
    "NLLB 目标语言（可多选，默认英语/波斯语/法语）",
    options=nllb_target_options,
    default=[],
    format_func=lambda x: language_key_to_zh.get(x, x),
    key="s4_nllb_targets",
    help="未选择时，系统默认翻译为英语、波斯语、法语。",
)
user_inputs["madlad400_input"] = st.text_area(
    "MADLAD-400 输入",
    value="病人在晚饭前没有吃药，而是在医生查房后才服用。",
    height=80,
    key="s4_madlad",
)
user_inputs["madlad400_target_langs"] = st.multiselect(
    "MADLAD-400 目标语言（可多选）",
    options=["english", "chinese", "persian", "french", "arabic", "hindi", "spanish", "russian", "german"],
    default=["chinese"],
    format_func=lambda x: language_key_to_zh.get(x, x),
    key="s4_madlad_targets",
)
user_inputs["aya_input"] = st.text_area(
    "Aya 输入",
    value="Design a cross-lingual evaluation protocol that balances fairness, cost, and pedagogical clarity.",
    height=80,
    key="s4_aya",
)
user_inputs["aya_langs"] = st.multiselect(
    "Aya 回答语言（可多选）",
    options=language_keys,
    default=["chinese"],
    format_func=lambda x: language_key_to_zh.get(x, x),
    key="s4_aya_langs",
)

if st.button("运行第四阶段测试", type="primary", use_container_width=True):
    with st.spinner("正在运行模型"):
        try:
            results = run_demo(user_inputs)
            st.markdown("### 运行结果")
            render_stage_results_dashboard(results, stage_title="stage4")
        except Exception as exc:
            st.error(str(exc))

st.markdown("---")
render_section_banner("第二部分：Benchmark 测评", "支持单模型评测和多模型多语言横向矩阵对比。")
render_stage_benchmark_panel(stage_id=4)
