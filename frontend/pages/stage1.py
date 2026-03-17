import streamlit as st
import sys
from pathlib import Path

project_root = Path(__file__).parent.parent.parent
sys.path.append(str(project_root))

from common.io_utils import load_markdown
from stage1.demo import run_demo

st.set_page_config(page_title="第一阶段：从 word2vec 到 BERT", layout="wide")
st.title("第一阶段：从 word2vec 到 BERT——预训练范式的奠基")

stage_dir = project_root / "stage1"

col1, col2 = st.columns(2)

with col1:
    st.subheader("阶段提纲")
    st.markdown(load_markdown(stage_dir / "outline.md"))
    
    st.subheader("阶段综述")
    st.markdown(load_markdown(stage_dir / "notes.md"))

with col2:
    st.subheader("本阶段模型列表")
    st.markdown(load_markdown(stage_dir / "models.md"))
    st.write("**模型目录结构：**")
    models_dir = stage_dir / "models"
    if models_dir.exists():
        st.write([d.name for d in models_dir.iterdir() if d.is_dir()])
    
    if st.button("▶ 运行本阶段 Demo", type="primary"):
        with st.spinner("正在运行本阶段的所有模型 Demo... 时间可能较长，请稍候。"):
            results = run_demo()
            for r in results:
                st.write(f"### {r['model']}")
                if not r['success']:
                    st.error(f"运行失败: {r['result']}")
                elif r['is_placeholder']:
                    st.info(f"说明性占位: {r['result']}")
                else:
                    st.success("运行成功！")
                    st.json(r['result'])
