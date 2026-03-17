import sys
from pathlib import Path
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

from common.io_utils import save_json
from stage3.models.mt5.run import run_mt5
from stage3.models.bloom.run import run_bloom
from stage3.models.mbart.run import run_mbart
from stage3.models.xglm.run import run_xglm
from stage3.models.gpt3.run import run_gpt3
from stage3.models.palm.run import run_palm

def run_demo():
    output_dir = Path(__file__).parent / "outputs"
    output_dir.mkdir(parents=True, exist_ok=True)
    results = [run_mt5(), run_bloom(), run_mbart(), run_xglm(), run_gpt3(), run_palm()]
    save_json({"stage": 3, "results": results}, output_dir / "latest_result.json")
    return results

if __name__ == '__main__':
    run_demo()
