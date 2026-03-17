import sys; from pathlib import Path; sys.path.append(str(Path(__file__).parent.parent.parent.parent)); from common.io_utils import save_json; from common.utils import build_model_result
def run_mbart():
    output_dir = Path(__file__).parent / "outputs"; output_dir.mkdir(parents=True, exist_ok=True)
    result = build_model_result("mBART", True, "多语言 BART 架构，适合机器翻译等任务，本地模型较重，仅作说明。", True)
    save_json(result, output_dir / "latest_result.json")
    return result
if __name__ == '__main__': print(run_mbart())
