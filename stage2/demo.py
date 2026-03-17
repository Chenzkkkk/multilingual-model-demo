import sys
from pathlib import Path
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

from common.io_utils import save_json
from stage2.models.mbert.run import run_mbert
from stage2.models.xlmr.run import run_xlmr
from stage2.models.xlm.run import run_xlm

def run_demo():
    output_dir = Path(__file__).parent / "outputs"
    output_dir.mkdir(parents=True, exist_ok=True)
    results = [run_mbert(), run_xlmr(), run_xlm()]
    save_json({"stage": 2, "results": results}, output_dir / "latest_result.json")
    return results

if __name__ == '__main__':
    run_demo()
