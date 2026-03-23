"""
mBERT - Multilingual BERT
多语言掩码语言模型演示
"""
import sys
from pathlib import Path

project_root = Path(__file__).parent.parent.parent.parent
sys.path.append(str(project_root))

from common.io_utils import save_json
from common.utils import build_model_result

def run_mbert(user_input: str = None):
    """
    mBERT 多语言掩码语言模型演示
    支持100+种语言
    用户需要在输入中包含 [MASK] 标记
    """
    output_dir = Path(__file__).parent / "outputs"
    output_dir.mkdir(parents=True, exist_ok=True)
    
    try:
        from transformers import pipeline
        
        # 如果没有用户输入，使用示例
        if not user_input:
            user_input = "我们 去 [MASK] 玩。"
        
        # 检查是否包含 [MASK]
        if "[MASK]" not in user_input:
            return build_model_result(
                "mBERT", 
                False, 
                "错误：输入必须包含 [MASK] 标记。例如：'我们 去 [MASK] 玩。' 或 'We are going to [MASK].'",
                user_input=user_input,
                input_type="text"
            )
        
        model_name = "bert-base-multilingual-cased"
        fill_mask = pipeline("fill-mask", model=model_name)
        
        # 执行掩码填充
        outputs = fill_mask(user_input, top_k=5)
        
        # 格式化输出
        results = [
            {
                "rank": i + 1,
                "token": o["token_str"].strip(),
                "score": float(o["score"])
            }
            for i, o in enumerate(outputs)
        ]
        
        result = build_model_result(
            "mBERT",
            True,
            {
                "model_info": "Multilingual BERT (Devlin et al., 2018)",
                "languages_supported": "100+ languages",
                "task": "Masked Language Modeling (MLM) - Multilingual",
                "input": user_input,
                "predictions": results
            },
            user_input=user_input,
            input_type="text"
        )
        save_json(result, output_dir / "latest_result.json")
        return result
        
    except Exception as e:
        result = build_model_result("mBERT", False, str(e), user_input=user_input)
        save_json(result, output_dir / "latest_result.json")
        return result

if __name__ == "__main__":
    run_mbert()
