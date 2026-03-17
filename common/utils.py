from pathlib import Path

def get_project_root() -> Path:
    return Path(__file__).parent.parent

def build_model_result(model_name: str, success: bool, output: str | dict, is_placeholder: bool = False) -> dict:
    return {
        "model": model_name,
        "success": success,
        "is_placeholder": is_placeholder,
        "result": output
    }
