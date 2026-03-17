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
