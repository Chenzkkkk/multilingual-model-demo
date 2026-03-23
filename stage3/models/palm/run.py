"""
PaLM - Pathways Language Model (Google)
谷歌 PaLM 模型
"""
import sys
from pathlib import Path

project_root = Path(__file__).parent.parent.parent.parent
sys.path.append(str(project_root))

from common.io_utils import save_json
from common.utils import build_model_result


def run_palm(user_input: str = None):
    """
    PaLM 模型
    注意: Google PaLM 没有官方开源版本
    """
    output_dir = Path(__file__).parent / "outputs"
    output_dir.mkdir(parents=True, exist_ok=True)
    
    error_message = (
        "❌ PaLM 模型不可用（无开源版本）\n\n"
        "Google 的 PaLM 是一个专有大规模语言模型，没有开源权重版本。\n\n"
        "使用方式:\n"
        "1. 通过 Google Vertex AI API 调用\n"
        "   - 需要 Google Cloud 账户和 API 密钥\n"
        "   - 参考: https://cloud.google.com/ai/generative-ai\n\n"
        "2. 使用开源替代模型:\n"
        "   - BLOOM (本项目有实现)\n"
        "   - LLaMA / Mistral\n"
        "   - Falcon\n"
        "   - Qwen\n\n"
        "如需启用实际 PaLM 调用，请:\n"
        "- 在 .env 中配置 GOOGLE_API_KEY\n"
        "- 修改此文件以使用 Google Generative AI SDK"
    )
    
    result = build_model_result(
        "PaLM",
        False,
        error_message,
        user_input=user_input,
        input_type="text"
    )
    save_json(result, output_dir / "latest_result.json")
    return result


if __name__ == "__main__":
    print(run_palm())

