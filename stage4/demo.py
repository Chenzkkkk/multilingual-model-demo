import sys
from pathlib import Path
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

from common.io_utils import save_json
from stage4.models.qwen.run import run_qwen
from stage4.models.clip.run import run_clip
from stage4.models.gpt4o.run import run_gpt4o
from stage4.models.claude.run import run_claude

import importlib
ph_models = ["llama", "deepseek", "hunyuan", "afrolm", "serengeti", "seallm", "multilingual_clip"]
ph_funcs = []
for ph in ph_models:
    mod = importlib.import_module(f"stage4.models.{ph}.run")
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
