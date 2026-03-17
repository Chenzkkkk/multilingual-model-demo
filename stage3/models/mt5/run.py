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
