"""
GPT-3 - Generative Pre-trained Transformer 3 (OpenAI)
OpenAI GPT-3 模型
"""
import sys
import os
from pathlib import Path

project_root = Path(__file__).parent.parent.parent.parent
sys.path.append(str(project_root))

from common.io_utils import save_json
from common.utils import build_model_result


def run_gpt3(user_input: str = None):
    """
    GPT-3 模型
    注意: GPT-3 是 OpenAI 的专有模型，需要 API 密钥
    """
    output_dir = Path(__file__).parent / "outputs"
    output_dir.mkdir(parents=True, exist_ok=True)
    
    text = user_input or "Say hello in Spanish"
    
    # 检查 API 密钥
    api_key = os.environ.get('OPENAI_API_KEY')
    if not api_key or api_key.strip() == "":
        error_message = (
            "❌ GPT-3 模型不可用（需要 OpenAI API）\n\n"
            "GPT-3 是 OpenAI 的专有大规模语言模型。\n\n"
            "启用步骤:\n"
            "1. 获取 OpenAI API 密钥\n"
            "   - 访问 https://platform.openai.com/api-keys\n"
            "   - 创建新的 API 密钥\n\n"
            "2. 配置环境变量\n"
            "   - 在 .env 文件中设置: OPENAI_API_KEY=sk-...\n\n"
            "3. 费用提示\n"
            "   - OpenAI API 按 token 计费\n"
            "   - 查看定价: https://openai.com/pricing\n\n"
            "开源替代方案（本项目已包含）:\n"
            "- BLOOM (facebook 开源大模型)\n"
            "- XGLM (多语言生成模型)\n"
            "- LLaMA / Mistral\n"
            "- Qwen (阿里巴巴)\n"
        )
        result = build_model_result("GPT-3", False, error_message, user_input=text, input_type="text")
        save_json(result, output_dir / "latest_result.json")
        return result
    
    # 如果有 API 密钥，尝试调用
    try:
        import openai
        openai.api_key = api_key
        
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful multilingual assistant."},
                {"role": "user", "content": text}
            ],
            max_tokens=100,
            temperature=0.7
        )
        
        output_text = response['choices'][0]['message']['content']
        
        result = build_model_result(
            "GPT-3",
            True,
            {
                "model": "gpt-3.5-turbo",
                "input": text,
                "output": output_text,
                "usage": response['usage']
            },
            user_input=text,
            input_type="text"
        )
        save_json(result, output_dir / "latest_result.json")
        return result
        
    except Exception as e:
        error_msg = f"OpenAI API 调用失败: {str(e)}\n\n请检查:\n1. API 密钥是否有效\n2. 网络连接\n3. 账户是否有充足额度"
        result = build_model_result("GPT-3", False, error_msg, user_input=text, input_type="text")
        save_json(result, output_dir / "latest_result.json")
        return result


if __name__ == "__main__":
    print(run_gpt3())

