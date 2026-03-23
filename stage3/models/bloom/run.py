from transformers import pipeline
import sys
import os
from pathlib import Path

# 设置模型缓存目录  
os.environ.setdefault('HF_HOME', './models')

project_root = Path(__file__).parent.parent.parent.parent
sys.path.append(str(project_root))

from common.io_utils import save_json
from common.utils import build_model_result

def run_bloom(user_input: str = None):
    output_dir = Path(__file__).parent / "outputs"
    output_dir.mkdir(parents=True, exist_ok=True)
    try:
        model_name = "bigscience/bloom-560m"
        generator = pipeline("text-generation", model=model_name, max_new_tokens=15, model_kwargs={'cache_dir': os.environ.get('HF_HOME')})
        text = user_input or "Bonjour, comment allez"
        out = generator(text)
        result = build_model_result(
            "BLOOM",
            True,
            {"input": text, "output": out[0]["generated_text"]},
            user_input=text,
            input_type="text",
        )
        save_json(result, output_dir / "latest_result.json")
        return result
    except Exception as e:
        result = build_model_result("BLOOM", False, str(e), user_input=user_input)
        save_json(result, output_dir / "latest_result.json")
        return result

if __name__ == '__main__':
    print(run_bloom())
