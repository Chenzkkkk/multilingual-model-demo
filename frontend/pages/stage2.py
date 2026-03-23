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
    "第二阶段讲解：多语言 Encoder 预训练",
    "本阶段关注跨语言共享表示与零样本迁移，强调多语言理解任务下的泛化能力对比。",
)

stage_dir = project_root / "stage2"

st.markdown("### 本阶段测试模型")
st.markdown("XLM, XLM-R")

col1, col2 = st.columns(2)
with col1:
    st.markdown("### 阶段纲要")
    st.markdown(load_markdown(stage_dir / "outline.md").replace("→", "到"))
with col2:
    st.markdown("### 详细讲解")
    st.markdown(load_markdown(stage_dir / "notes.md").replace("→", "到"))

st.markdown("### 进入测试")
if st.button("进入第二阶段测试页面", use_container_width=True):
    st.switch_page("pages/stage2_test.py")
