import os
from pathlib import Path

root = Path(r"e:\大数据处理技术\multilingual-pre-trained")

def write_file(rel_path, content):
    p = root / rel_path
    p.parent.mkdir(parents=True, exist_ok=True)
    with open(p, "w", encoding="utf-8") as f:
        f.write(content.strip() + "\n")

# ==========================================
# STAGE 2
# ==========================================
write_file('stage2/README.md', """
# 第二阶段：mBERT / XLM / XLM-R——多语言 Encoder 预训练时代

本阶段展示了早期深度预训练模型在多语言任务中的扩展，着重于 Encoder-only 架构。
主要代表包括 mBERT (多语言 BERT)、XLM (跨语言语言模型，引入 TLM) 以及 XLM-Roberta。
""")

write_file('stage2/outline.md', """
- 多语言语料构建与词表共享
- mBERT 的零样本跨语言迁移现象
- XLM：引入 Translation Language Modeling (TLM)
- XLM-R：基于 RoBERTa 架构在大规模多语言语料上的训练
""")

write_file('stage2/notes.md', """
第二阶段是多语言 Encoder 预训练的爆发期。
- **mBERT** 直接将 104 种语言的维基百科数据混合训练，意外地获得了极强的跨语言迁移能力。
- **XLM** 尝试通过平行语料引入 TLM 目标，显式在不同语言间建立对齐关系。
- **XLM-R** 证明了只要语料足够大（100种语言的 CommonCrawl）、模型容量足够大，即使没有平行语料的 MLM 目标也能超越依靠平行语料的模型，确立了大规模自监督学习的作用。
""")

write_file('stage2/models.md', """
| 模型 | 架构 | 定位 | 本地可运行 | 示例方式 | 仅说明 |
| :-- | :-- | :-- | :-- | :-- | :-- |
| mBERT | Transformer Encoder | 多语言基线 | 是 | fill-mask | 否 |
| XLM-R | Transformer Encoder | 大规模多语言 RoBERTa | 是 | fill-mask | 否 |
| XLM | Transformer Encoder | 引入翻译目标 | 否 | 说明性占位 | 是 |
""")

write_file('stage2/models/mbert/run.py', """
from transformers import pipeline
import sys
from pathlib import Path

project_root = Path(__file__).parent.parent.parent.parent
sys.path.append(str(project_root))

from common.io_utils import save_json
from common.utils import build_model_result

def run_mbert():
    output_dir = Path(__file__).parent / "outputs"
    output_dir.mkdir(parents=True, exist_ok=True)
    try:
        model_name = "bert-base-multilingual-cased"
        fill_mask = pipeline("fill-mask", model=model_name)
        text = "Paris es la capital de [MASK]."
        out = fill_mask(text, top_k=2)
        results = [{"token": o["token_str"], "score": float(o["score"])} for o in out]
        result = build_model_result("mBERT (Stage 2)", True, {"input": text, "output": results})
        save_json(result, output_dir / "latest_result.json")
        return result
    except Exception as e:
        result = build_model_result("mBERT (Stage 2)", False, str(e))
        save_json(result, output_dir / "latest_result.json")
        return result

if __name__ == '__main__':
    print(run_mbert())
""")

write_file('stage2/models/xlmr/run.py', """
from transformers import pipeline
import sys
from pathlib import Path

project_root = Path(__file__).parent.parent.parent.parent
sys.path.append(str(project_root))

from common.io_utils import save_json
from common.utils import build_model_result

def run_xlmr():
    output_dir = Path(__file__).parent / "outputs"
    output_dir.mkdir(parents=True, exist_ok=True)
    try:
        model_name = "xlm-roberta-base"
        fill_mask = pipeline("fill-mask", model=model_name)
        text = "It is a very <mask> day."
        out = fill_mask(text, top_k=2)
        results = [{"token": o["token_str"], "score": float(o["score"])} for o in out]
        result = build_model_result("XLM-R", True, {"input": text, "output": results})
        save_json(result, output_dir / "latest_result.json")
        return result
    except Exception as e:
        result = build_model_result("XLM-R", False, str(e))
        save_json(result, output_dir / "latest_result.json")
        return result

if __name__ == '__main__':
    print(run_xlmr())
""")

write_file('stage2/models/xlm/run.py', """
import sys
from pathlib import Path
project_root = Path(__file__).parent.parent.parent.parent
sys.path.append(str(project_root))
from common.io_utils import save_json
from common.utils import build_model_result

def run_xlm():
    output_dir = Path(__file__).parent / "outputs"
    output_dir.mkdir(parents=True, exist_ok=True)
    explanation = "XLM 引入了翻译语言模型 (TLM) 目标，在具有平行语料的跨语言理解上有重要地位。本地运行较重且已被 XLM-R 超越，故此处仅作说明性占位。"
    result = build_model_result("XLM", True, explanation, is_placeholder=True)
    save_json(result, output_dir / "latest_result.json")
    return result

if __name__ == '__main__':
    print(run_xlm())
""")

write_file('stage2/demo.py', """
import sys
from pathlib import Path
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

from common.io_utils import save_json
from models.mbert.run import run_mbert
from models.xlmr.run import run_xlmr
from models.xlm.run import run_xlm

def run_demo():
    output_dir = Path(__file__).parent / "outputs"
    output_dir.mkdir(parents=True, exist_ok=True)
    results = [run_mbert(), run_xlmr(), run_xlm()]
    save_json({"stage": 2, "results": results}, output_dir / "latest_result.json")
    return results

if __name__ == '__main__':
    run_demo()
""")


# ==========================================
# STAGE 3
# ==========================================
write_file('stage3/README.md', """
# 第三阶段：从 mT5 到 BLOOM——多语言生成的双路线过渡期

本阶段标志着多语言模型从单纯的表示学习（Encoder）向生成能力（Encoder-Decoder 和 Decoder-only）过渡。
涵盖了 mT5、mBART，以及大规模多语言自回归模型 BLOOM、XGLM 等。
""")

write_file('stage3/outline.md', """
- 从 Encoder 向 Seq2Seq 架构的转变 (mT5, mBART)
- 多文档、多语言的无监督生成目标
- 走向 Decoder-only 架构 (GPT-3, PaLM 的多语言涌现)
- 多语言开源巨星：BLOOM 与 XGLM
""")

write_file('stage3/notes.md', """
在预训练发展中期，自然语言处理逐步收敛到文本生成任务。
- **mT5 / mBART** 采用 Encoder-Decoder 架构，统一了多语言的理解和生成任务，如翻译和摘要。
- 随后，**GPT-3** 的出现展示了大规模 Decoder-only 模型的 Few-shot 学习能力。
- 为了推动多语言社区发展，BigScience 团队开源了支持 46 种语言和 13 种编程语言的 **BLOOM** 模型，成为当时最大的多语言开源 LLM 之一。
""")

write_file('stage3/models.md', """
| 模型 | 架构 | 定位 | 本地可运行 | 示例方式 | 仅说明 |
| :-- | :-- | :-- | :-- | :-- | :-- |
| mT5 | Encoder-Decoder | 多语种 T5 扩展 | 是 | text2text-generation | 否 |
| BLOOM | Decoder-only | 开源多语言巨无霸 | 是 | text-generation (560m) | 否 |
| mBART | Encoder-Decoder | 多语种生成 | 否 | 说明性占位 | 是 |
| XGLM | Decoder-only | 多语跨语言生成 | 否 | 说明性占位 | 是 |
| GPT-3 | Decoder-only | 大模型时代先驱 | 否 | 说明性占位 | 是 |
| PaLM | Decoder-only | 涌现多语言能力 | 否 | 说明性占位 | 是 |
""")

write_file('stage3/models/mt5/run.py', """
from transformers import pipeline
import sys
from pathlib import Path

project_root = Path(__file__).parent.parent.parent.parent
sys.path.append(str(project_root))

from common.io_utils import save_json
from common.utils import build_model_result

def run_mt5():
    output_dir = Path(__file__).parent / "outputs"
    output_dir.mkdir(parents=True, exist_ok=True)
    try:
        model_name = "google/mt5-small"
        generator = pipeline("text2text-generation", model=model_name, max_length=20)
        text = "translate English to French: Good morning"
        out = generator(text)
        result = build_model_result("mT5", True, {"input": text, "output": out[0]['generated_text']})
        save_json(result, output_dir / "latest_result.json")
        return result
    except Exception as e:
        result = build_model_result("mT5", False, str(e))
        save_json(result, output_dir / "latest_result.json")
        return result

if __name__ == '__main__':
    print(run_mt5())
""")

write_file('stage3/models/bloom/run.py', """
from transformers import pipeline
import sys
from pathlib import Path

project_root = Path(__file__).parent.parent.parent.parent
sys.path.append(str(project_root))

from common.io_utils import save_json
from common.utils import build_model_result

def run_bloom():
    output_dir = Path(__file__).parent / "outputs"
    output_dir.mkdir(parents=True, exist_ok=True)
    try:
        model_name = "bigscience/bloom-560m"
        generator = pipeline("text-generation", model=model_name, max_new_tokens=15)
        text = "Bonjour, comment allez"
        out = generator(text)
        result = build_model_result("BLOOM", True, {"input": text, "output": out[0]['generated_text']})
        save_json(result, output_dir / "latest_result.json")
        return result
    except Exception as e:
        result = build_model_result("BLOOM", False, str(e))
        save_json(result, output_dir / "latest_result.json")
        return result

if __name__ == '__main__':
    print(run_bloom())
""")

write_file('stage3/models/mbart/run.py', """
import sys; from pathlib import Path; sys.path.append(str(Path(__file__).parent.parent.parent.parent)); from common.io_utils import save_json; from common.utils import build_model_result
def run_mbart():
    output_dir = Path(__file__).parent / "outputs"; output_dir.mkdir(parents=True, exist_ok=True)
    result = build_model_result("mBART", True, "多语言 BART 架构，适合机器翻译等任务，本地模型较重，仅作说明。", True)
    save_json(result, output_dir / "latest_result.json")
    return result
if __name__ == '__main__': print(run_mbart())
""")

write_file('stage3/models/xglm/run.py', """
import sys; from pathlib import Path; sys.path.append(str(Path(__file__).parent.parent.parent.parent)); from common.utils import build_model_result; from common.io_utils import save_json
def run_xglm():
    result = build_model_result("XGLM", True, "Facebook 提出的基于 Decoder 的多语言模型，本地运行较重，仅作说明。", True)
    output_dir = Path(__file__).parent / "outputs"; output_dir.mkdir(parents=True, exist_ok=True); save_json(result, output_dir / "latest_result.json")
    return result
""")

write_file('stage3/models/gpt3/run.py', """
import sys; from pathlib import Path; sys.path.append(str(Path(__file__).parent.parent.parent.parent)); from common.utils import build_model_result; from common.io_utils import save_json
def run_gpt3():
    result = build_model_result("GPT-3", True, "作为开启大语言模型范式的里程碑，它在少量多语言数据上展现了涌现的翻译能力，为闭源，仅作说明。", True)
    output_dir = Path(__file__).parent / "outputs"; output_dir.mkdir(parents=True, exist_ok=True); save_json(result, output_dir / "latest_result.json")
    return result
""")

write_file('stage3/models/palm/run.py', """
import sys; from pathlib import Path; sys.path.append(str(Path(__file__).parent.parent.parent.parent)); from common.utils import build_model_result; from common.io_utils import save_json
def run_palm():
    result = build_model_result("PaLM", True, "Google 的庞大语言模型，证明了扩大参数规模能极大提升多语言推理能力。无开源权重，仅作说明。", True)
    output_dir = Path(__file__).parent / "outputs"; output_dir.mkdir(parents=True, exist_ok=True); save_json(result, output_dir / "latest_result.json")
    return result
""")

write_file('stage3/demo.py', """
import sys
from pathlib import Path
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

from common.io_utils import save_json
from models.mt5.run import run_mt5
from models.bloom.run import run_bloom
from models.mbart.run import run_mbart
from models.xglm.run import run_xglm
from models.gpt3.run import run_gpt3
from models.palm.run import run_palm

def run_demo():
    output_dir = Path(__file__).parent / "outputs"
    output_dir.mkdir(parents=True, exist_ok=True)
    results = [run_mt5(), run_bloom(), run_mbart(), run_xglm(), run_gpt3(), run_palm()]
    save_json({"stage": 3, "results": results}, output_dir / "latest_result.json")
    return results

if __name__ == '__main__':
    run_demo()
""")


# ==========================================
# STAGE 4
# ==========================================
write_file('stage4/README.md', """
# 第四阶段：GPT-4 之后——多语言 LLM 的对齐、涌现与前沿

本阶段展示当代最先进的多语言大模型及其前沿方向，包括对齐指令微调后的多模态/多语言混合大模型。
""")

write_file('stage4/outline.md', """
- SFT 和 RLHF 在多语言模型中的应用
- 小参数模型的崛起：Qwen, Llama 3 等
- 闭源旗舰 API：GPT-4o, Claude 3
- 多模态多语言能力：CLIP 及演进
- 区域语言及特殊语系：AfroLM, SeaLLM
""")

write_file('stage4/notes.md', """
在第四阶段，大规模无监督预训练的基础上加入了指令微调（SFT）和对齐（RLHF）。
- **参数效能极大提升**：现在的如 Qwen2.5 等开源模型可以在相对较小的参数下匹敌早期的大参数模型。
- **视觉多模态大融合**：CLIP 等模型统一了多模态表征，多语言甚至也可以作为其中的模态之一。
- **区域化语言深耕**：SeaLLM 等专门针对东南亚等资源匮乏语系做了适配。
""")

write_file('stage4/models.md', """
| 模型 | 架构 | 定位 | 本地可运行 | 示例方式 | 仅说明 |
| :-- | :-- | :-- | :-- | :-- | :-- |
| Qwen | Decoder-only | 高效多语种对话 | 是 | text-generation (0.5B) | 否 |
| CLIP | 多模态 | 多模态图文对齐 | 是 | zero-shot-image-classification | 否 |
| GPT-4o | Decoder-only | 云端最强闭源 | 是 | OpenAI API | 否 |
| Claude | Decoder-only | 云端最强闭源 | 是 | Anthropic API | 否 |
| Llama | Decoder-only | 社区标杆 | 否 | 说明性占位 | 是 |
| SeaLLM | Decoder-only | 东南亚多语种 | 否 | 说明性占位 | 是 |
""")

write_file('stage4/models/qwen/run.py', """
from transformers import pipeline
import sys
from pathlib import Path

project_root = Path(__file__).parent.parent.parent.parent
sys.path.append(str(project_root))

from common.io_utils import save_json
from common.utils import build_model_result

def run_qwen():
    output_dir = Path(__file__).parent / "outputs"
    output_dir.mkdir(parents=True, exist_ok=True)
    try:
        model_name = "Qwen/Qwen2.5-0.5B-Instruct"
        pipe = pipeline("text-generation", model=model_name, max_new_tokens=20)
        messages = [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "你好，请用一句话介绍你自己。"},
        ]
        out = pipe(messages)
        result = build_model_result("Qwen (0.5B)", True, {"input": "你好", "output": out[0]['generated_text'][-1]['content']})
        save_json(result, output_dir / "latest_result.json")
        return result
    except Exception as e:
        result = build_model_result("Qwen (0.5B)", False, str(e))
        save_json(result, output_dir / "latest_result.json")
        return result

def main():
    print(run_qwen())
""")

write_file('stage4/models/clip/run.py', """
from transformers import pipeline
import sys
from pathlib import Path

project_root = Path(__file__).parent.parent.parent.parent
sys.path.append(str(project_root))

from common.io_utils import save_json
from common.utils import build_model_result

def run_clip():
    output_dir = Path(__file__).parent / "outputs"
    output_dir.mkdir(parents=True, exist_ok=True)
    try:
        model_name = "openai/clip-vit-base-patch32"
        pipe = pipeline("zero-shot-image-classification", model=model_name)
        url = "http://images.cocodataset.org/val2017/000000039769.jpg"
        candidate_labels = ["a photo of a cat", "a photo of a dog"]
        out = pipe(url, candidate_labels=candidate_labels)
        
        cleaned_out = [{"label": o["label"], "score": round(o["score"], 4)} for o in out]
        result = build_model_result("CLIP", True, {"image_url": url, "output": cleaned_out})
        save_json(result, output_dir / "latest_result.json")
        return result
    except Exception as e:
        result = build_model_result("CLIP", False, str(e))
        save_json(result, output_dir / "latest_result.json")
        return result
""")

write_file('stage4/models/gpt4o/run.py', """
import sys
from pathlib import Path

project_root = Path(__file__).parent.parent.parent.parent
sys.path.append(str(project_root))

from common.api_utils import get_openai_client
from common.io_utils import save_json
from common.utils import build_model_result

def run_gpt4o():
    output_dir = Path(__file__).parent / "outputs"
    output_dir.mkdir(parents=True, exist_ok=True)
    
    client = get_openai_client()
    if not client:
        result = build_model_result("GPT-4o", False, "未配置 API Key，跳过真实调用。")
        save_json(result, output_dir / "latest_result.json")
        return result
        
    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": "Say short hello in Spanish"}],
            max_tokens=10
        )
        result = build_model_result("GPT-4o", True, {"input": "Say short hello in Spanish", "output": response.choices[0].message.content})
        save_json(result, output_dir / "latest_result.json")
        return result
    except Exception as e:
        result = build_model_result("GPT-4o", False, str(e))
        save_json(result, output_dir / "latest_result.json")
        return result
""")

write_file('stage4/models/claude/run.py', """
import sys
from pathlib import Path

project_root = Path(__file__).parent.parent.parent.parent
sys.path.append(str(project_root))

from common.api_utils import get_anthropic_client
from common.io_utils import save_json
from common.utils import build_model_result

def run_claude():
    output_dir = Path(__file__).parent / "outputs"
    output_dir.mkdir(parents=True, exist_ok=True)
    
    client = get_anthropic_client()
    if not client:
        result = build_model_result("Claude", False, "未配置 API Key，跳过真实调用。")
        save_json(result, output_dir / "latest_result.json")
        return result
        
    try:
        response = client.messages.create(
            model="claude-3-haiku-20240307",
            max_tokens=20,
            messages=[{"role": "user", "content": "Say short hello in French"}]
        )
        result = build_model_result("Claude", True, {"input": "Say short hello in French", "output": response.content[0].text})
        save_json(result, output_dir / "latest_result.json")
        return result
    except Exception as e:
        result = build_model_result("Claude", False, str(e))
        save_json(result, output_dir / "latest_result.json")
        return result
""")

# Placeholders for stage4
for ph in ["llama", "deepseek", "hunyuan", "afrolm", "serengeti", "seallm", "multilingual_clip"]:
    write_file(f'stage4/models/{ph}/run.py', f'''
import sys; from pathlib import Path; sys.path.append(str(Path(__file__).parent.parent.parent.parent)); from common.utils import build_model_result; from common.io_utils import save_json
def run_model():
    result = build_model_result("{ph}", True, "因本地资源或 API 限制，当前仅作说明性占位，详细可参考文档。", True)
    output_dir = Path(__file__).parent / "outputs"; output_dir.mkdir(parents=True, exist_ok=True); save_json(result, output_dir / "latest_result.json")
    return result
''')

write_file('stage4/demo.py', """
import sys
from pathlib import Path
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

from common.io_utils import save_json
from models.qwen.run import run_qwen
from models.clip.run import run_clip
from models.gpt4o.run import run_gpt4o
from models.claude.run import run_claude

import importlib
ph_models = ["llama", "deepseek", "hunyuan", "afrolm", "serengeti", "seallm", "multilingual_clip"]
ph_funcs = []
for ph in ph_models:
    mod = importlib.import_module(f"models.{ph}.run")
    ph_funcs.append(mod.run_model)

def run_demo():
    output_dir = Path(__file__).parent / "outputs"
    output_dir.mkdir(parents=True, exist_ok=True)
    
    results = [run_qwen(), run_clip(), run_gpt4o(), run_claude()]
    for fn in ph_funcs:
        results.append(fn())
        
    save_json({"stage": 4, "results": results}, output_dir / "latest_result.json")
    return results

if __name__ == '__main__':
    run_demo()
""")

# ==========================================
# UPDATE FRONTEND PAGES
# ==========================================
for i in range(2, 5):
    write_file(f'frontend/pages/stage{i}.py', f'''
import streamlit as st
import sys
from pathlib import Path

project_root = Path(__file__).parent.parent.parent
sys.path.append(str(project_root))

from common.io_utils import load_markdown
try:
    if {i} == 2:
        from stage2.demo import run_demo
    elif {i} == 3:
        from stage3.demo import run_demo
    elif {i} == 4:
        from stage4.demo import run_demo
except ImportError:
    st.error("Demo module not found!")
    def run_demo(): return []

st.set_page_config(page_title=f"第{i}阶段", layout="wide")
st.title(f"第{i}阶段")

stage_dir = project_root / f"stage{i}"

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
        with st.spinner("运行中...时间可能较长，请稍候。"):
            results = run_demo()
            for r in results:
                st.write(f"### {{r['model']}}")
                if not r['success']:
                    st.error(f"运行失败: {{r['result']}}")
                elif r.get('is_placeholder'):
                    st.info(f"说明性占位: {{r['result']}}")
                else:
                    st.success("运行成功！")
                    st.json(r['result'])
''')

print("All stage files generated nicely.")
