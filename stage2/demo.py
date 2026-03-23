import sys
from pathlib import Path

project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

from common.io_utils import save_json
from stage2.models.xlm.run import run_xlm
from stage2.models.xlmr.run import run_xlmr

def run_demo(user_inputs: dict = None):
    """运行Stage 2的所有模型演示"""
    output_dir = Path(__file__).parent / "outputs"
    output_dir.mkdir(parents=True, exist_ok=True)
    
    user_inputs = user_inputs or {}
    
    results = [
        run_xlm(user_input=user_inputs.get("xlm_input")),
        run_xlmr(user_input=user_inputs.get("xlmr_input"))
    ]
    
    save_json({"stage": 2, "results": results}, output_dir / "latest_result.json")
    return results

if __name__ == "__main__":
    run_demo()
