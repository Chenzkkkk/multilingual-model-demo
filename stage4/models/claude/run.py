import sys
from pathlib import Path

project_root = Path(__file__).parent.parent.parent.parent
sys.path.append(str(project_root))

from common.api_utils import get_anthropic_client
from common.io_utils import save_json
from common.utils import build_model_result

def run_claude():
    output_dir = Path(__file__).parent / "outputs"
    output_dir.mkdir(parents=True, exist_ok=True)
    
    client = get_anthropic_client()
    if not client:
        result = build_model_result("Claude", False, "未配置 API Key，跳过真实调用。")
        save_json(result, output_dir / "latest_result.json")
        return result
        
    try:
        response = client.messages.create(
            model="claude-3-haiku-20240307",
            max_tokens=20,
            messages=[{"role": "user", "content": "Say short hello in French"}]
        )
        result = build_model_result("Claude", True, {"input": "Say short hello in French", "output": response.content[0].text})
        save_json(result, output_dir / "latest_result.json")
        return result
    except Exception as e:
        result = build_model_result("Claude", False, str(e))
        save_json(result, output_dir / "latest_result.json")
        return result
