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
