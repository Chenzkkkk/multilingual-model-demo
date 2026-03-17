import sys
from pathlib import Path

project_root = Path(__file__).parent.parent.parent.parent
sys.path.append(str(project_root))

from common.api_utils import get_openai_client
from common.io_utils import save_json
from common.utils import build_model_result

def run_gpt4o():
    output_dir = Path(__file__).parent / "outputs"
    output_dir.mkdir(parents=True, exist_ok=True)
    
    client = get_openai_client()
    if not client:
        result = build_model_result("GPT-4o", False, "未配置 API Key，跳过真实调用。")
        save_json(result, output_dir / "latest_result.json")
        return result
        
    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": "Say short hello in Spanish"}],
            max_tokens=10
        )
        result = build_model_result("GPT-4o", True, {"input": "Say short hello in Spanish", "output": response.choices[0].message.content})
        save_json(result, output_dir / "latest_result.json")
        return result
    except Exception as e:
        result = build_model_result("GPT-4o", False, str(e))
        save_json(result, output_dir / "latest_result.json")
        return result
