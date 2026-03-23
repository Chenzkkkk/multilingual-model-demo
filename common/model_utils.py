import os
from pathlib import Path


def get_model_cache_dir() -> str:
    """返回统一的本地模型缓存目录（绝对路径）。"""
    project_root = Path(__file__).parent.parent
    raw = os.getenv("MODEL_CACHE_DIR") or os.getenv("HF_HOME") or "./models"
    cache_dir = Path(raw)
    if not cache_dir.is_absolute():
        cache_dir = (project_root / cache_dir).resolve()
    cache_dir.mkdir(parents=True, exist_ok=True)
    return str(cache_dir)


def configure_hf_cache_env() -> str:
    """统一配置 HuggingFace 缓存环境变量，确保后续运行复用本地模型。"""
    cache_dir = get_model_cache_dir()
    os.environ["HF_HOME"] = cache_dir
    os.environ["MODEL_CACHE_DIR"] = cache_dir
    os.environ["TRANSFORMERS_CACHE"] = cache_dir
    os.environ["HUGGINGFACE_HUB_CACHE"] = cache_dir
    return cache_dir


def load_pipeline(task: str, model: str):
    """加载 huggingface pipeline，并强制使用本地缓存目录。"""
    try:
        from transformers import pipeline

        cache_dir = configure_hf_cache_env()
        return pipeline(task, model=model, model_kwargs={"cache_dir": cache_dir})
    except Exception:
        return None
