import sys
from pathlib import Path
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

from common.io_utils import save_json
from stage3.models.mbart.run import run_mbart
from stage3.models.mt5.run import run_mt5
from stage3.models.bloom.run import run_bloom
from stage3.models.xglm.run import run_xglm

def run_demo(user_inputs: dict = None):
    output_dir = Path(__file__).parent / "outputs"
    output_dir.mkdir(parents=True, exist_ok=True)
    
    user_inputs = user_inputs or {}
    
    results = [
        run_mbart(user_input=user_inputs.get("mbart_input")),
        run_mt5(user_input=user_inputs.get("mt5_input")),
        run_bloom(user_input=user_inputs.get("bloom_input")),
        run_xglm(user_input=user_inputs.get("xglm_input")),
    ]
    save_json({"stage": 3, "results": results}, output_dir / "latest_result.json")
    return results

if __name__ == '__main__':
    run_demo()
