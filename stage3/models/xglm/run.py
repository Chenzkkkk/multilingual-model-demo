"""
XGLM - Cross-lingual Generative Language Model
跨语言生成语言模型
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


def run_xglm(user_input: str = None):
    """
    XGLM 跨语言文本生成任务
    XGLM 是 Facebook 推出的生成型多语言模型
    """
    output_dir = Path(__file__).parent / "outputs"
    output_dir.mkdir(parents=True, exist_ok=True)
    
    text = user_input or "Hello, the weather is"
    
    try:
        from transformers import AutoTokenizer, AutoModelForCausalLM
        
        # 使用较小的模型版本以适应本地运行
        model_name = "facebook/xglm-564M"
        
        tokenizer = AutoTokenizer.from_pretrained(
            model_name,
            cache_dir=os.environ.get('HF_HOME'),
            trust_remote_code=True
        )
        model = AutoModelForCausalLM.from_pretrained(
            model_name,
            cache_dir=os.environ.get('HF_HOME'),
            trust_remote_code=True
        )
        
        # 生成文本
        input_ids = tokenizer.encode(text, return_tensors="pt")
        output = model.generate(input_ids, max_length=50, num_beams=3, early_stopping=True)
        generated_text = tokenizer.decode(output[0], skip_special_tokens=True)
        
        result = build_model_result(
            "XGLM",
            True,
            {
                "model": "facebook/xglm-564M",
                "task": "Cross-lingual Text Generation",
                "input": text,
                "output": generated_text,
                "languages_supported": "100+ languages"
            },
            user_input=text,
            input_type="text"
        )
        save_json(result, output_dir / "latest_result.json")
        return result
        
    except Exception as e:
        error_msg = (
            f"XGLM 模型加载失败: {str(e)}\n\n"
            f"解决方案:\n"
            f"1. 检查网络连接（首次需下载 ~2.4GB 模型文件）\n"
            f"2. 确保磁盘空间充足\n"
            f"3. 安装最新 transformers: pip install -U transformers\n"
            f"4. 检查 HF_HOME 环境变量设置"
        )
        result = build_model_result("XGLM", False, error_msg, user_input=text, input_type="text")
        save_json(result, output_dir / "latest_result.json")
        return result


if __name__ == "__main__":
    print(run_xglm())

