import sys; from pathlib import Path; sys.path.append(str(Path(__file__).parent.parent.parent.parent)); from common.utils import build_model_result; from common.io_utils import save_json
def run_xglm():
    result = build_model_result("XGLM", True, "Facebook 提出的基于 Decoder 的多语言模型，本地运行较重，仅作说明。", True)
    output_dir = Path(__file__).parent / "outputs"; output_dir.mkdir(parents=True, exist_ok=True); save_json(result, output_dir / "latest_result.json")
    return result
