import sys
from pathlib import Path

project_root = Path(__file__).resolve().parents[1]
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))
import streamlit as st

from frontend.ui_components import inject_base_styles, render_page_header

st.set_page_config(
    page_title="多语言预训练模型讲解与测试平台",
    layout="wide",
    initial_sidebar_state="expanded",
)

inject_base_styles()

render_page_header(
    "多语言预训练模型讲解与测试平台",
    "本平台用于课程讲解、模型对比和交互测试。点击阶段页面中的测试按钮，可进入独立测试界面。",
)

st.markdown("### 平台定位")
st.markdown(
    """
- 教学定位：按技术演进路径讲解多语言模型设计思想与代表模型。
- 实验定位：提供统一输入面板与结构化输出展示，用于快速比较模型行为。
- 工程定位：支持 API 模型和本地模型混合测试，便于课程和项目迭代。
"""
)

st.markdown("### 阶段与模型全览")

stage_catalog = {
    "第一阶段": {
        "主题": "词表示与预训练奠基",
        "模型": "Word2Vec, ELMo, Transformer, BERT, mBERT",
        "讲解页": "pages/stage1.py",
    },
    "第二阶段": {
        "主题": "多语言 Encoder 预训练",
        "模型": "XLM, XLM-R",
        "讲解页": "pages/stage2.py",
    },
    "第三阶段": {
        "主题": "多语言生成过渡期",
        "模型": "mBART, mT5, BLOOM, XGLM",
        "讲解页": "pages/stage3.py",
    },
    "第四阶段": {
        "主题": "对齐与涌现",
        "模型": "Qwen1, Qwen2, Qwen3, Qwen-MT, LLaMA4, NLLB, MADLAD-400, Aya",
        "讲解页": "pages/stage4.py",
    },
}

for idx, (stage_name, info) in enumerate(stage_catalog.items(), start=1):
    st.markdown(
        f"""
<div class="info-card">
  <h4 style="margin:0 0 0.45rem 0;color:#0f4c81;">{idx}. {stage_name} | {info['主题']}</h4>
  <p style="margin:0.2rem 0 0.45rem 0;"><strong>测试模型</strong>：{info['模型']}</p>
</div>
""",
        unsafe_allow_html=True,
    )
    if st.button(f"进入{stage_name}", key=f"guide_{idx}", use_container_width=True):
        st.switch_page(info["讲解页"])

st.markdown("### 使用说明")
st.markdown(
    """
1. 先进入某一阶段讲解页，了解该阶段模型背景、任务目标与适用边界。
2. 再进入对应测试页，填写输入并运行。
3. 结果页仅展示结构化摘要，不展示原始 JSON 响应，确保教学可读性。
4. API 模型请在 .env 中配置密钥，尤其是 DASHSCOPE_API_KEY 和 AIHUBMIX_API_KEY。
"""
)
