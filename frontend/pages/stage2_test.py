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
from stage2.demo import run_demo

inject_base_styles()

render_page_header(
    "第二阶段测试页面",
    "用于运行 XLM, XLM-R。建议使用中文与其他语言进行对照输入。",
)

st.markdown("### 本页测试模型")
st.markdown("XLM, XLM-R")

render_section_banner("第一部分：通俗测试与结果展示", "可直接演示跨语言输入在 XLM / XLM-R 上的输出差异。")

if st.button("返回第二阶段讲解", use_container_width=False):
    st.switch_page("pages/stage2.py")

models = {
    "xlm_input": ("XLM", "He said the policy was 'brilliant' | 他说这个政策“真是太高明了”，结果公司亏损创了新高。"),
    "xlmr_input": ("XLM-R", "虽然进度并不<mask>，团队还是在最后一周完成了交付。"),
}

user_inputs = {}
for key, (title, default_val) in models.items():
    with st.expander(f"{title} 输入", expanded=False):
        user_inputs[key] = st.text_area("输入", value=default_val, height=90, key=f"s2_{key}")

if st.button("运行第二阶段测试", type="primary", use_container_width=True):
    with st.spinner("正在运行模型"):
        try:
            results = run_demo(user_inputs)
            st.markdown("### 运行结果")
            render_stage_results_dashboard(results, stage_title="stage2")
        except Exception as exc:
            st.error(str(exc))

st.markdown("---")
render_section_banner("第二部分：Benchmark 测评", "在本阶段可用任务上做定量评测，并查看横向对比图。")
render_stage_benchmark_panel(stage_id=2)
