"""
mBART - Multilingual BART
多语言 BART 模型，用于翻译和生成任务
"""
import sys
import os
from pathlib import Path

project_root = Path(__file__).parent.parent.parent.parent
sys.path.append(str(project_root))

from common.io_utils import save_json
from common.utils import build_model_result

# 设置模型缓存目录
os.environ.setdefault('HF_HOME', './models')


def run_mbart(user_input: str = None):
    """
    mBART 多语言序列到序列任务
    支持翻译、摘要等生成任务
    """
    output_dir = Path(__file__).parent / "outputs"
    output_dir.mkdir(parents=True, exist_ok=True)
    
    text = user_input or "translate English to German: Hello, how are you?"
    
    try:
        from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
        
        # 使用 Facebook 的 mBART 模型
        model_name = "facebook/mbart-large-cc25"
        
        tokenizer = AutoTokenizer.from_pretrained(
            model_name,
            cache_dir=os.environ.get('HF_HOME'),
            trust_remote_code=True
        )
        model = AutoModelForSeq2SeqLM.from_pretrained(
            model_name,
            cache_dir=os.environ.get('HF_HOME'),
            trust_remote_code=True
        )
        
        # 解析输入格式：格式应为 "translate source to target: text"
        # 简化处理：自动检测语言并生成
        article_input = text
        
        input_ids = tokenizer(article_input, return_tensors="pt", truncation=True).input_ids
        output_ids = model.generate(input_ids, max_length=100, num_beams=3)
        output_text = tokenizer.decode(output_ids[0], skip_special_tokens=True)
        
        result = build_model_result(
            "mBART",
            True,
            {
                "model": "facebook/mbart-large-cc25",
                "task": "Sequence-to-Sequence Generation",
                "input": text,
                "output": output_text,
                "supported_languages": "25 languages"
            },
            user_input=text,
            input_type="text"
        )
        save_json(result, output_dir / "latest_result.json")
        return result
        
    except Exception as e:
        error_msg = (
            f"mBART 模型加载失败: {str(e)}\n\n"
            f"解决方案:\n"
            f"1. 检查网络连接（首次需下载 ~1.6GB 模型文件）\n"
            f"2. 确保磁盘空间充足\n"
            f"3. 安装最新 transformers: pip install -U transformers\n"
            f"4. 推荐输入格式: 'translate source_lang to target_lang: text'"
        )
        result = build_model_result("mBART", False, error_msg, user_input=text, input_type="text")
        save_json(result, output_dir / "latest_result.json")
        return result


if __name__ == '__main__':
    print(run_mbart())

