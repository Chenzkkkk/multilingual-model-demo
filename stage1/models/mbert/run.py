from transformers import pipeline
import sys
from pathlib import Path

project_root = Path(__file__).parent.parent.parent.parent
sys.path.append(str(project_root))

from common.io_utils import save_json
from common.utils import build_model_result
import json

def run_mbert():
    output_dir = Path(__file__).parent / "outputs"
    output_dir.mkdir(parents=True, exist_ok=True)
    
    try:
        model_name = "bert-base-multilingual-cased"
        fill_mask = pipeline("fill-mask", model=model_name)
        
        examples_file = Path(__file__).parent / "examples.json"
        
        texts = [
            "We are going to Paris [MASK].",
            "Paris es la capital de [MASK].",
            "今天天气很好，一起去[MASK]玩吧。"
        ]
        
        if examples_file.exists():
            with open(examples_file, "r", encoding="utf-8") as f:
                texts = json.load(f)["texts"]
                
        results = {}
        for text in texts:
            out = fill_mask(text, top_k=2)
            results[text] = [{"token_str": o["token_str"], "score": round(float(o["score"]), 4)} for o in out]
            
        result = build_model_result("mbert", True, results)
        save_json(result, output_dir / "latest_result.json")
        return result
    except Exception as e:
         result = build_model_result("mbert", False, str(e))
         save_json(result, output_dir / "latest_result.json")
         return result

if __name__ == "__main__":
    print(run_mbert())
