import sys
import os
from pathlib import Path

# 设置模型缓存目录
os.environ.setdefault('HF_HOME', './models')

project_root = Path(__file__).parent.parent.parent.parent
sys.path.append(str(project_root))

from common.io_utils import save_json
from common.utils import build_model_result
from common.model_utils import configure_hf_cache_env

def run_mt5(user_input: str = None):
    output_dir = Path(__file__).parent / "outputs"
    output_dir.mkdir(parents=True, exist_ok=True)
    cache_dir = configure_hf_cache_env()
    try:
        from transformers import AutoModelForSeq2SeqLM, AutoTokenizer

        model_name = "google/mt5-small"
        text = user_input or "translate English to French: Good morning"

        # mT5 依赖 sentencepiece，显式关闭 fast tokenizer 可避免部分环境下的解析异常
        tokenizer = AutoTokenizer.from_pretrained(model_name, cache_dir=cache_dir, use_fast=False)
        model = AutoModelForSeq2SeqLM.from_pretrained(model_name, cache_dir=cache_dir)
        model.eval()

        inputs = tokenizer(text, return_tensors="pt", truncation=True, max_length=256)
        output_ids = model.generate(
            **inputs,
            max_new_tokens=64,
            num_beams=4,
            early_stopping=True,
        )
        generated = tokenizer.decode(output_ids[0], skip_special_tokens=True)

        result = build_model_result(
            "mT5",
            True,
            {
                "input": text,
                "output": generated,
                "cache_dir": cache_dir,
            },
            user_input=text,
            input_type="text",
        )
        save_json(result, output_dir / "latest_result.json")
        return result
    except Exception as e:
        result = build_model_result("mT5", False, str(e), user_input=user_input)
        save_json(result, output_dir / "latest_result.json")
        return result

if __name__ == '__main__':
    print(run_mt5())
