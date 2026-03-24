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
from stage3.demo import run_demo

inject_base_styles()

render_page_header(
    "第三阶段测试页面",
    "用于运行 mBART, mT5, BLOOM, XGLM。",
)

st.markdown("### 本页测试模型")
st.markdown("mBART, mT5, BLOOM, XGLM")

render_section_banner("第一部分：通俗测试与结果展示", "聚焦多语言生成能力，观察翻译、续写、论述的差异。")

if st.button("返回第三阶段讲解", use_container_width=False):
    st.switch_page("pages/stage3.py")

models = {
    "mbart_input": ("mBART", "translate Chinese to English: 去年获奖的那位科学家回到了她曾经就读的那所大学，并宣布设立青年研究基金。"),
    "mt5_input": ("mT5", "translate Chinese to Persian: 这家公司在2024年售出了12540件产品，其中40%来自海外市场。"),
    "bloom_input": ("BLOOM", "请以记者口吻写一段100字新闻快讯，主题是“多语言模型在医疗问答中的应用边界”。"),
    "xglm_input": ("XGLM", "Write a short bilingual paragraph (Chinese + English) comparing translation quality and reasoning quality in multilingual models."),
}

user_inputs = {}
for key, (title, default_val) in models.items():
    with st.expander(f"{title} 输入", expanded=False):
        user_inputs[key] = st.text_area("输入", value=default_val, height=90, key=f"s3_{key}")

if st.button("运行第三阶段测试", type="primary", use_container_width=True):
    with st.spinner("正在运行模型"):
        try:
            results = run_demo(user_inputs)
            st.markdown("### 运行结果")
            render_stage_results_dashboard(results, stage_title="stage3")
        except Exception as exc:
            st.error(str(exc))

st.markdown("---")
render_section_banner("第二部分：Benchmark 测评", "可执行翻译、推理任务测评，并得到矩阵图表。")
render_stage_benchmark_panel(stage_id=3)
