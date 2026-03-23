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
    "第一阶段讲解：从 Word2Vec 到 BERT",
    "本阶段讲解词向量、上下文化表示与预训练范式的建立过程。建议先阅读讲解，再进入独立测试页。",
)

stage_dir = project_root / "stage1"

st.markdown("### 本阶段测试模型")
st.markdown("Word2Vec, ELMo, Transformer, BERT, mBERT")

col_a, col_b = st.columns(2)
with col_a:
    st.markdown("### 阶段纲要")
    st.markdown(load_markdown(stage_dir / "outline.md").replace("→", "到"))

with col_b:
    st.markdown("### 详细讲解")
    st.markdown(load_markdown(stage_dir / "notes.md").replace("→", "到"))

st.markdown("### 进入测试")
st.markdown("点击下方按钮进入独立测试页面。")
if st.button("进入第一阶段测试界面", use_container_width=True):
    st.switch_page("pages/stage1_test.py")
