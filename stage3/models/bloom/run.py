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
