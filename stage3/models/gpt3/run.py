import sys; from pathlib import Path; sys.path.append(str(Path(__file__).parent.parent.parent.parent)); from common.utils import build_model_result; from common.io_utils import save_json
def run_gpt3():
    result = build_model_result("GPT-3", True, "作为开启大语言模型范式的里程碑，它在少量多语言数据上展现了涌现的翻译能力，为闭源，仅作说明。", True)
    output_dir = Path(__file__).parent / "outputs"; output_dir.mkdir(parents=True, exist_ok=True); save_json(result, output_dir / "latest_result.json")
    return result
