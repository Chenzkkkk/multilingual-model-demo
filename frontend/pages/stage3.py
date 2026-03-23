import sys
from pathlib import Path

import streamlit as st

project_root = Path(__file__).resolve().parents[2]
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from common.io_utils import load_markdown
from frontend.ui_components import inject_base_styles, render_page_header


inject_base_styles()

render_page_header(
    "第三阶段讲解：多语言生成过渡期",
    "本阶段围绕 mBART 和 mT5 到 BLOOM 与 XGLM 的代际变化，说明多语言生成任务中的模型结构与能力边界。",
)

stage_dir = project_root / "stage3"

st.markdown("### 本阶段测试模型")
st.markdown("mBART, mT5, BLOOM, XGLM")

col1, col2 = st.columns(2)
with col1:
    st.markdown("### 阶段纲要")
    st.markdown(load_markdown(stage_dir / "outline.md").replace("→", "到"))
with col2:
    st.markdown("### 详细讲解")
    st.markdown(load_markdown(stage_dir / "notes.md").replace("→", "到"))

st.markdown("### 进入测试")
if st.button("进入第三阶段测试页面", use_container_width=True):
    st.switch_page("pages/stage3_test.py")
