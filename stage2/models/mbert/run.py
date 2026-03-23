"""
mBERT - Multilingual BERT (Stage 2)
多语言Encoder预训练的开端
"""
import sys
import os
from pathlib import Path

# 设置模型缓存目录
os.environ.setdefault('HF_HOME', './models')
project_root = Path(__file__).parent.parent.parent.parent
sys.path.append(str(project_root))

from common.io_utils import save_json
from common.utils import build_model_result
from common.model_utils import configure_hf_cache_env

def run_mbert(user_input: str = None):
    """Stage 2 的 mBERT (西班牙语示例)"""
    output_dir = Path(__file__).parent / "outputs"
    output_dir.mkdir(parents=True, exist_ok=True)
    cache_dir = configure_hf_cache_env()
    
    try:
        import torch
        from transformers import AutoModelForMaskedLM, AutoTokenizer
        
        if not user_input:
            user_input = "Paris es la capital de [MASK]."
        
        if "[MASK]" not in user_input:
            result = build_model_result(
                "mBERT (Stage 2)", False, 
                "输入必须包含 [MASK] 标记",
                user_input=user_input
            )
            save_json(result, output_dir / "latest_result.json")
            return result
        
        model_name = "bert-base-multilingual-cased"
        tokenizer = AutoTokenizer.from_pretrained(model_name, cache_dir=cache_dir)
        model = AutoModelForMaskedLM.from_pretrained(model_name, cache_dir=cache_dir)
        model.eval()

        encoded = tokenizer(user_input, return_tensors="pt")
        mask_token_id = tokenizer.mask_token_id
        mask_positions = (encoded["input_ids"][0] == mask_token_id).nonzero(as_tuple=True)[0]
        if len(mask_positions) == 0:
            raise ValueError("输入中未找到 [MASK] 标记")

        with torch.no_grad():
            logits = model(**encoded).logits

        mask_pos = int(mask_positions[0].item())
        probs = torch.softmax(logits[0, mask_pos], dim=-1)
        top_scores, top_ids = torch.topk(probs, k=5)

        results = []
        for i, (token_id, score) in enumerate(zip(top_ids.tolist(), top_scores.tolist())):
            results.append(
                {
                    "rank": i + 1,
                    "token": tokenizer.decode([token_id]).strip(),
                    "score": float(score),
                }
            )
        
        result = build_model_result(
            "mBERT (Stage 2)", True,
            {
                "model_info": "Multilingual BERT (2018)",
                "task": "多语言MLM",
                "input": user_input,
                "cache_dir": cache_dir,
                "predictions": results
            },
            user_input=user_input,
            input_type="text"
        )
        save_json(result, output_dir / "latest_result.json")
        return result
        
    except Exception as e:
        result = build_model_result("mBERT (Stage 2)", False, str(e), user_input=user_input)
        save_json(result, output_dir / "latest_result.json")
        return result

if __name__ == "__main__":
    run_mbert()
