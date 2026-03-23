import sys
from pathlib import Path

import streamlit as st

project_root = Path(__file__).resolve().parents[2]
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from frontend.ui_components import inject_base_styles, render_model_result, render_page_header
from stage2.demo import run_demo

inject_base_styles()

render_page_header(
    "第二阶段测试页面",
    "用于运行 XLM, XLM-R。建议使用中文与其他语言进行对照输入。",
)

st.markdown("### 本页测试模型")
st.markdown("XLM, XLM-R")

if st.button("返回第二阶段讲解", use_container_width=False):
    st.switch_page("pages/stage2.py")

models = {
    "xlm_input": ("XLM", "The weather is nice | 天气很好"),
    "xlmr_input": ("XLM-R", "今天是一个很<mask>的日子。"),
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
            for result in results:
                render_model_result(result)
        except Exception as exc:
            st.error(str(exc))
