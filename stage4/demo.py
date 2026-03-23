import sys
from pathlib import Path

project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

from common.io_utils import save_json

def run_demo(user_inputs: dict = None):
    """运行Stage 4的所有模型演示"""
    output_dir = Path(__file__).parent / "outputs"
    output_dir.mkdir(parents=True, exist_ok=True)
    
    user_inputs = user_inputs or {}
    results = []
    
    # Qwen 系列
    models_to_run = [
        "qwen1", "qwen2", "qwen3", "qwen_mt",  
        "llama4",  
        "nllb", "madlad400", "aya"  
    ]
    
    for model in models_to_run:
        try:
            mod = __import__(f"stage4.models.{model}.run", fromlist=["run_" + model.replace("-", "_")])
            func_name = f"run_{model.replace('-', '_')}"
            if hasattr(mod, func_name):
                run_func = getattr(mod, func_name)
                if model == "qwen_mt":
                    result = run_func(
                        user_input=user_inputs.get("qwen_mt_input"),
                        source_lang=user_inputs.get("qwen_mt_source_lang") or "Chinese",
                        target_lang=user_inputs.get("qwen_mt_target_lang") or "English",
                        domains=user_inputs.get("qwen_mt_domains") or "General",
                    )
                else:
                    result = run_func(user_input=user_inputs.get(f"{model}_input"))
                results.append(result)
        except Exception as e:
            results.append(
                {
                    "model": model,
                    "success": False,
                    "is_placeholder": False,
                    "result": str(e),
                }
            )
    
    save_json({"stage": 4, "results": results}, output_dir / "latest_result.json")
    return results

if __name__ == '__main__':
    run_demo()
