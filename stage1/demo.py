import sys
from pathlib import Path

project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

from common.io_utils import save_json
from stage1.models.word2vec.run import run_word2vec
from stage1.models.elmo.run import run_elmo
from stage1.models.bert.run import run_bert
from stage1.models.mbert.run import run_mbert

def run_demo():
    output_dir = Path(__file__).parent / "outputs"
    output_dir.mkdir(parents=True, exist_ok=True)
    
    results = [
        run_word2vec(),
        run_elmo(),
        run_bert(),
        run_mbert()
    ]
    
    save_json({"stage": 1, "results": results}, output_dir / "latest_result.json")
    return results

if __name__ == "__main__":
    run_demo()
