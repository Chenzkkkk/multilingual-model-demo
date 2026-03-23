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
    "第四阶段讲解：对齐与涌现",
    "本阶段聚焦指令对齐、推理增强和多语言助手能力，模型调用以 API 为主，强调课堂可操作性与工程可迁移性。",
)

stage_dir = project_root / "stage4"

st.markdown("### 本阶段测试模型")
st.markdown("Qwen1, Qwen2, Qwen3, Qwen-MT, LLaMA4, NLLB, MADLAD-400, Aya")

col1, col2 = st.columns(2)
with col1:
    st.markdown("### 阶段纲要")
    st.markdown(load_markdown(stage_dir / "outline.md").replace("→", "到"))
with col2:
    st.markdown("### 详细讲解")
    st.markdown(load_markdown(stage_dir / "notes.md").replace("→", "到"))

st.markdown("### 进入测试")
if st.button("进入第四阶段测试页面", use_container_width=True):
    st.switch_page("pages/stage4_test.py")
