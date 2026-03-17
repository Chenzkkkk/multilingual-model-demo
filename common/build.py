import os
from pathlib import Path

root = Path(__file__).parent.parent

def write_file(rel_path, content):
    p = root / rel_path
    p.parent.mkdir(parents=True, exist_ok=True)
    with open(p, 'w', encoding='utf-8') as f:
        f.write(content.strip() + '\n')

# ==========================================
# STAGE 2
# ==========================================
write_file('stage2/README.md', '''
# 第二阶段：mBERT / XLM / XLM-R——多语言 Encoder 预训练时代

本阶段展示早期深度预训练模型在多语言任务中的扩展，着重于 Encoder-only 架构。
主要代表包括 mBERT、XLM 以及 XLM-Roberta。
''')

write_file('stage2/outline.md', '''
- 多语言语料构建与词表共享
- mBERT 的零样本跨语言迁移现象
- XLM：引入 Translation Language Modeling (TLM)
- XLM-R：基于 RoBERTa 架构大规模多语言预训练
''')

write_file('stage2/notes.md', '''
第二阶段是多语言 Encoder 预训练爆发期。
- **mBERT** 让不同语言共享同一个特征空间，获得了零样本跨语言能力。
- **XLM** 尝试通过平行语料引入 TLM 目标，显式建立跨语言对齐关系。
- **XLM-R** 证明了只要多语言单语语料规模足够大、模型容量足够大，即使只有纯 MLM 也能超越之前依赖双语语料的模型，确立了大规模自监督的作用。
''')

write_file('stage2/models.md', '''
| 模型 | 架构 | 定位 | 本地可运行 | 示例方式 | 仅说明 |
| :-- | :-- | :-- | :-- | :-- | :-- |
| mBERT | Transformer Encoder | 多语言基线 | 是 | fill-mask | 否 |
| XLM-R | Transformer Encoder | 大规模 RoBERTa | 是 | fill-mask | 否 |
| XLM | Transformer Encoder | 引入翻译目标 | 否 | 说明性占位 | 是 |
''')

write_file('stage2/models/mbert/run.py', '''
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
    run_mbert()
''')

write_file('stage2/models/xlmr/run.py', '''
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
    run_xlmr()
''')

write_file('stage2/models/xlm/run.py', '''
import sys
from pathlib import Path
project_root = Path(__file__).parent.parent.parent.parent
sys.path.append(str(project_root))
from common.io_utils import save_json
from common.utils import build_model_result

def run_xlm():
    output_dir = Path(__file__).parent / "outputs"
    output_dir.mkdir(parents=True, exist_ok=True)
    explanation = "XLM 引入了 TLM 目标，但在实践中已被更大规模的无监督模型(XLM-R)取代，且加载开销较大，故此处仅作说明性占位。"
    result = build_model_result("XLM", True, explanation, is_placeholder=True)
    save_json(result, output_dir / "latest_result.json")
    return result

if __name__ == '__main__':
    run_xlm()
''')

write_file('stage2/demo.py', '''
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
''')

# ==========================================
# STAGE 3
# ==========================================
write_file('stage3/README.md', '''
# 第三阶段：从 mT5 到 BLOOM——多语言生成的双路线过渡期

标志多语言大模型从单一的 Encoder 过渡到了统一生成（Seq2Seq 和 Decoder-only）架构。
''')

write_file('stage3/outline.md', '''
- 从 Encoder 到 Encoder-Decoder (mT5, mBART)
- Decoder-only 架构占据主导 (GPT-3 展现多语言涌现)
- 多源开源巨型模型发力：BLOOM 和 XGLM
''')

write_file('stage3/notes.md', '''
- **mT5 / mBART** 使用 Encoder-Decoder 结构，在涉及多语言文本生成时大放异彩。
- **BLOOM** 作为社区共同推进的开源多语言模型典范，参数量大，多语种支持极好，确立了自回归大预言模型的优势。
- **GPT-3 / PaLM** 等闭源模型显示了庞大参数带来的“零样本多语言推理涌现”。
''')

write_file('stage3/models.md', '''
| 模型 | 架构 | 定位 | 本地可运行 | 示例方式 | 仅说明 |
| :-- | :-- | :-- | :-- | :-- | :-- |
| mT5 | Encoder-Decoder | 多语种 T5 扩展 | 是 | text2text-generation | 否 |
| BLOOM | Decoder-only | 开源多语言巨无霸 | 是 | text-generation (560m) | 否 |
| mBART | Encoder-Decoder | 多语种生成 | 否 | 说明性占位 | 是 |
| XGLM | Decoder-only | 多语跨语言生成 | 否 | 说明性占位 | 是 |
| GPT-3 | Decoder-only | 闭源大模型先驱 | 否 | 说明性占位 | 是 |
| PaLM | Decoder-only | 涌现多语言能力 | 否 | 说明性占位 | 是 |
''')

write_file('stage3/models/mt5/run.py', '''
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
        generator = pipeline("text2text-generation", model=model_name, max_new_tokens=15)
        text = "translate English to German: Good morning"
        out = generator(text)
        result = build_model_result("mT5", True, {"input": text, "output": out[0]['generated_text']})
        save_json(result, output_dir / "latest_result.json")
        return result
    except Exception as e:
        result = build_model_result("mT5", False, str(e))
        save_json(result, output_dir / "latest_result.json")
        return result

if __name__ == '__main__':
    run_mt5()
''')

write_file('stage3/models/bloom/run.py', '''
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
        generator = pipeline("text-generation", model=model_name, max_new_tokens=10)
        text = "Bonjour, je m'appelle"
        out = generator(text)
        result = build_model_result("BLOOM", True, {"input": text, "output": out[0]['generated_text']})
        save_json(result, output_dir / "latest_result.json")
        return result
    except Exception as e:
        result = build_model_result("BLOOM", False, str(e))
        save_json(result, output_dir / "latest_result.json")
        return result

if __name__ == '__main__':
    run_bloom()
''')

for m in ["mbart", "xglm", "gpt3", "palm"]:
    write_file(f'stage3/models/{m}/run.py', f'''
import sys
from pathlib import Path
project_root = Path(__file__).parent.parent.parent.parent
sys.path.append(str(project_root))
from common.utils import build_model_result
from common.io_utils import save_json

def run_{m}():
    output_dir = Path(__file__).parent / "outputs"
    output_dir.mkdir(parents=True, exist_ok=True)
    result = build_model_result("{m.upper()}", True, "因资源或闭源原因，在此仅作说明性占位。", is_placeholder=True)
    save_json(result, output_dir / "latest_result.json")
    return result
if __name__ == '__main__':
    run_{m}()
''')

write_file('stage3/demo.py', '''
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
''')

# ==========================================
# STAGE 4
# ==========================================
write_file('stage4/README.md', '''
# 第四阶段：GPT-4 之后——多语言 LLM 的对齐、涌现与前沿

深入如今的最前沿大模型，结合 SFT 和 RLHF 等技术，多语言模型甚至多模态对齐大模型成为主流。
''')

write_file('stage4/outline.md', '''
- 精细化对齐与多语言性能提升
- Qwen, Llama 系本地小参数模型的极限性能
- 区域定制：SeaLLM 等
- 跨模态跨语言能力统一：CLIP
''')

write_file('stage4/notes.md', '''
进入到大模型前沿期：
- **微型模型(Small Small LMs)** 如 Qwen 系列，使用超强数据清洗技术让 0.5B 的模型也具备多语言基础对话能力。
- **多模态**：CLIP 提供了图文匹配，进一步有 Multilingual-CLIP 等将图像引入跨语言。
- **API 级大物**：GPT-4o 和 Claude 垄断了云端全能榜单，它们无需特定语种训练也可以极好支持小语种和各种泛翻译任务。
''')

write_file('stage4/models.md', '''
| 模型 | 架构 | 定位 | 本地可运行 | 示例方式 | 仅说明 |
| :-- | :-- | :-- | :-- | :-- | :-- |
| Qwen | Decoder-only | 高效多语种对话 | 是 | text-generation (0.5B) | 否 |
| CLIP | 多模态 | 图片-多语言对齐 | 是 | zero-shot图像分类 | 否 |
| GPT-4o | Decoder-only | 云端最强闭源 | 是 | OpenAI API | 否 |
| Claude | Decoder-only | 云端最强闭源 | 是 | Anthropic API | 否 |
| 其他 | - | - | 否 | 说明性占位 | 是 |
''')

write_file('stage4/models/qwen/run.py', '''
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
        pipe = pipeline("text-generation", model=model_name, max_new_tokens=15)
        # 兼容最新 pipeline chat 格式
        messages = [{"role": "user", "content": "用一句话介绍你自己"}]
        out = pipe(messages)
        result = build_model_result("Qwen (0.5B)", True, {"input": "用一句话介绍你自己", "output": out[0]['generated_text'][-1]['content']})
        save_json(result, output_dir / "latest_result.json")
        return result
    except Exception as e:
        result = build_model_result("Qwen (0.5B)", False, str(e))
        save_json(result, output_dir / "latest_result.json")
        return result

if __name__ == '__main__':
    run_qwen()
''')

write_file('stage4/models/clip/run.py', '''
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
        candidate_labels = ["cat", "dog", "car"]
        out = pipe(url, candidate_labels=candidate_labels)
        
        cleaned_out = [{"label": o["label"], "score": round(o["score"], 4)} for o in out]
        result = build_model_result("CLIP", True, {"image_url": url, "output": cleaned_out})
        save_json(result, output_dir / "latest_result.json")
        return result
    except Exception as e:
        result = build_model_result("CLIP", False, str(e))
        save_json(result, output_dir / "latest_result.json")
        return result

if __name__ == '__main__':
    run_clip()
''')

write_file('stage4/models/gpt4o/run.py', '''
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
        result = build_model_result("GPT-4o", False, "未配置真实 API Key，跳过调用。")
        save_json(result, output_dir / "latest_result.json")
        return result
        
    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": "Say 'hello' in French"}],
            max_tokens=10
        )
        result = build_model_result("GPT-4o", True, {"input": "Say 'hello' in French", "output": response.choices[0].message.content})
        save_json(result, output_dir / "latest_result.json")
        return result
    except Exception as e:
        result = build_model_result("GPT-4o", False, str(e))
        save_json(result, output_dir / "latest_result.json")
        return result

if __name__ == '__main__':
    run_gpt4o()
''')

write_file('stage4/models/claude/run.py', '''
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
        result = build_model_result("Claude", False, "未配置真实 API Key，跳过调用。")
        save_json(result, output_dir / "latest_result.json")
        return result
        
    try:
        response = client.messages.create(
            model="claude-3-haiku-20240307",
            max_tokens=20,
            messages=[{"role": "user", "content": "Say 'hello' in Spanish"}]
        )
        result = build_model_result("Claude", True, {"input": "Say 'hello' in Spanish", "output": response.content[0].text})
        save_json(result, output_dir / "latest_result.json")
        return result
    except Exception as e:
        result = build_model_result("Claude", False, str(e))
        save_json(result, output_dir / "latest_result.json")
        return result

if __name__ == '__main__':
    run_claude()
''')

ph_models = ["llama", "deepseek", "hunyuan", "afrolm", "serengeti", "seallm", "multilingual_clip"]
for ph in ph_models:
    write_file(f'stage4/models/{ph}/run.py', f'''
import sys
from pathlib import Path
project_root = Path(__file__).parent.parent.parent.parent
sys.path.append(str(project_root))
from common.utils import build_model_result
from common.io_utils import save_json

def run_{ph}():
    output_dir = Path(__file__).parent / "outputs"
    output_dir.mkdir(parents=True, exist_ok=True)
    result = build_model_result("{ph.upper()}", True, "说明性占位，当前模型本地执行代价较高或为前沿特化路线。", is_placeholder=True)
    save_json(result, output_dir / "latest_result.json")
    return result

if __name__ == '__main__':
    run_{ph}()
''')

write_file('stage4/demo.py', '''
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

def run_demo():
    output_dir = Path(__file__).parent / "outputs"
    output_dir.mkdir(parents=True, exist_ok=True)
    
    results = [run_qwen(), run_clip(), run_gpt4o(), run_claude()]
    
    for ph in ph_models:
        mod = importlib.import_module(f"models.{ph}.run")
        results.append(getattr(mod, f"run_{ph}")())
        
    save_json({"stage": 4, "results": results}, output_dir / "latest_result.json")
    return results

if __name__ == '__main__':
    run_demo()
''')
