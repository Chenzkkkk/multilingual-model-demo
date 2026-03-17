import sys
from pathlib import Path
project_root = Path(__file__).parent.parent.parent.parent
sys.path.append(str(project_root))
from common.io_utils import save_json
from common.utils import build_model_result

def run_xlm():
    output_dir = Path(__file__).parent / "outputs"
    output_dir.mkdir(parents=True, exist_ok=True)
    explanation = "XLM 引入了翻译语言模型 (TLM) 目标，在具有平行语料的跨语言理解上有重要地位。本地运行较重且已被 XLM-R 超越，故此处仅作说明性占位。"
    result = build_model_result("XLM", True, explanation, is_placeholder=True)
    save_json(result, output_dir / "latest_result.json")
    return result

if __name__ == '__main__':
    print(run_xlm())
