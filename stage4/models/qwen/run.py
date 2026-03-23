import sys
from pathlib import Path

project_root = Path(__file__).parent.parent.parent.parent
sys.path.append(str(project_root))

from stage4.models.runtime import run_qwen_api_chat

def run_qwen(user_input: str = None):
    output_dir = Path(__file__).parent / "outputs"
    return run_qwen_api_chat(
        model_label="Qwen (0.5B)",
        model_id="qwen-plus",
        output_dir=output_dir,
        user_input=user_input,
        default_input="你好，请用一句话介绍你自己。",
        temperature=0.7,
    )

def main():
    print(run_qwen())
