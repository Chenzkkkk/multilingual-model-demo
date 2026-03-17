from transformers import pipeline

def load_pipeline(task: str, model: str):
    """加载 huggingface 管道模型"""
    try:
        classifier = pipeline(task, model=model)
        return classifier
    except Exception as e:
        return None
