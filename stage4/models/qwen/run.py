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
