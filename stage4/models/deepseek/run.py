import sys; from pathlib import Path; sys.path.append(str(Path(__file__).parent.parent.parent.parent)); from common.utils import build_model_result; from common.io_utils import save_json
def run_model():
    result = build_model_result("deepseek", True, "因本地资源或 API 限制，当前仅作说明性占位，详细可参考文档。", True)
    output_dir = Path(__file__).parent / "outputs"; output_dir.mkdir(parents=True, exist_ok=True); save_json(result, output_dir / "latest_result.json")
    return result
