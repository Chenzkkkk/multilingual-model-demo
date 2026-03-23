import sys
from pathlib import Path

import streamlit as st

project_root = Path(__file__).resolve().parents[2]
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from frontend.ui_components import inject_base_styles, render_model_result, render_page_header
from stage3.demo import run_demo

inject_base_styles()

render_page_header(
    "第三阶段测试页面",
    "用于运行 mBART, mT5, BLOOM, XGLM。",
)

st.markdown("### 本页测试模型")
st.markdown("mBART, mT5, BLOOM, XGLM")

if st.button("返回第三阶段讲解", use_container_width=False):
    st.switch_page("pages/stage3.py")

models = {
    "mbart_input": ("mBART", "translate Chinese to English: 你好，世界"),
    "mt5_input": ("mT5", "translate English to Chinese: Hello world"),
    "bloom_input": ("BLOOM", "今天天气很好，我想"),
    "xglm_input": ("XGLM", "今天天气很好，我想"),
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
            for result in results:
                render_model_result(result)
        except Exception as exc:
            st.error(str(exc))
