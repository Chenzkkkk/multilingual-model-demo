"""
XLM - Cross-lingual Language Model
跨语言语言模型（使用XLM-R进行多语言处理）
"""
import sys
import os
from pathlib import Path

project_root = Path(__file__).parent.parent.parent.parent
sys.path.append(str(project_root))

from common.io_utils import save_json
from common.utils import build_model_result
from common.model_utils import configure_hf_cache_env

# 设置模型缓存目录
os.environ.setdefault('HF_HOME', './models')

def run_xlm(user_input: str = None):
    """
    XLM 多语言语义相似度计算任务
    使用 XLM-R 模型对多语言文本进行处理
    """
    output_dir = Path(__file__).parent / "outputs"
    output_dir.mkdir(parents=True, exist_ok=True)
    cache_dir = configure_hf_cache_env()
    
    # 默认输入：两段不同语言的类似文本对
    text1 = "The weather is nice today"
    text2 = "天气今天很好"
    
    if user_input:
        # 如果用户提供输入，假设是用 | 分隔的两个文本
        if "|" in user_input:
            parts = user_input.split("|")
            text1 = parts[0].strip()
            text2 = parts[1].strip() if len(parts) > 1 else text2
        else:
            text1 = user_input
    
    try:
        from transformers import AutoTokenizer, AutoModel
        import torch
        
        # 使用 XLM-R 基础模型进行多语言处理
        model_name = "xlm-roberta-base"
        tokenizer = AutoTokenizer.from_pretrained(model_name, cache_dir=cache_dir)
        model = AutoModel.from_pretrained(model_name, cache_dir=cache_dir)
        
        # 编码两个文本
        encoded1 = tokenizer(text1, return_tensors='pt', truncation=True, max_length=128)
        encoded2 = tokenizer(text2, return_tensors='pt', truncation=True, max_length=128)
        
        # 获取输出表示
        with torch.no_grad():
            outputs1 = model(**encoded1)
            outputs2 = model(**encoded2)
        
        # 使用 [CLS] token 的表示计算相似度
        cls1 = outputs1.last_hidden_state[:, 0, :]  # [CLS] 表示
        cls2 = outputs2.last_hidden_state[:, 0, :]
        
        # 计算余弦相似度
        similarity = torch.nn.functional.cosine_similarity(cls1, cls2)
        similarity_score = float(similarity.item())
        
        result = build_model_result(
            "XLM",
            True,
            {
                "model_used": "xlm-roberta-base",
                "task": "Cross-lingual Text Similarity",
                "text1": text1,
                "text2": text2,
                "output": f"跨语言语义相似度: {round(similarity_score, 4)}",
                "similarity_score": round(similarity_score, 4),
                "cache_dir": cache_dir,
                "note": "Similarity score ranges from -1 to 1 (1 = identical meaning)"
            },
            user_input=user_input or f"{text1} | {text2}",
            input_type="text"
        )
        save_json(result, output_dir / "latest_result.json")
        return result
        
    except Exception as e:
        error_msg = f"模型加载失败: {str(e)}\n\n尝试修复:\n1. 检查网络连接\n2. 确保 transformers>=4.20.0\n3. 检查 HF_HOME 缓存目录权限"
        result = build_model_result(
            "XLM",
            False,
            error_msg,
            user_input=user_input,
            input_type="text"
        )
        save_json(result, output_dir / "latest_result.json")
        return result


if __name__ == "__main__":
    print(run_xlm())

