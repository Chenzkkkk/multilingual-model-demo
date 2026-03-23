"""
XLM-R - XLM-RoBERTa
100+种语言的大规模多语言RoBERTa模型
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

def run_xlmr(user_input: str = None):
    """
    XLM-R 多语言掩码填充任务
    """
    output_dir = Path(__file__).parent / "outputs"
    output_dir.mkdir(parents=True, exist_ok=True)
    cache_dir = configure_hf_cache_env()
    
    try:
        import torch
        from transformers import AutoModelForMaskedLM, AutoTokenizer
        
        if not user_input:
            user_input = "It is a very <mask> day."
        
        if "<mask>" not in user_input:
            result = build_model_result(
                "XLM-R", False,
                "输入必须包含 <mask> 标记（注意是尖括号）",
                user_input=user_input
            )
            save_json(result, output_dir / "latest_result.json")
            return result
        
        model_name = "xlm-roberta-base"
        tokenizer = AutoTokenizer.from_pretrained(model_name, cache_dir=cache_dir)
        model = AutoModelForMaskedLM.from_pretrained(model_name, cache_dir=cache_dir)
        model.eval()

        encoded = tokenizer(user_input, return_tensors="pt")
        mask_token_id = tokenizer.mask_token_id
        mask_positions = (encoded["input_ids"][0] == mask_token_id).nonzero(as_tuple=True)[0]
        if len(mask_positions) == 0:
            raise ValueError("输入中未找到 <mask> 标记")

        with torch.no_grad():
            logits = model(**encoded).logits

        mask_pos = int(mask_positions[0].item())
        probs = torch.softmax(logits[0, mask_pos], dim=-1)
        contains_cjk = any("\u4e00" <= ch <= "\u9fff" for ch in user_input)
        if contains_cjk:
            top_scores, top_ids = torch.topk(probs, k=200)
        else:
            top_scores, top_ids = torch.topk(probs, k=20)

        candidates = []
        for token_id, score in zip(top_ids.tolist(), top_scores.tolist()):
            token = tokenizer.decode([token_id]).strip()
            if not token:
                continue
            candidates.append({"token": token, "score": float(score)})

        results = []
        if contains_cjk:
            for item in candidates:
                token = item["token"]
                if any("\u4e00" <= ch <= "\u9fff" for ch in token):
                    results.append(item)
                if len(results) >= 5:
                    break

        if len(results) < 5:
            for item in candidates:
                if item in results:
                    continue
                results.append(item)
                if len(results) >= 5:
                    break

        final_results = []
        for i, item in enumerate(results[:5], start=1):
            final_results.append(
                {
                    "rank": i,
                    "token": item["token"],
                    "score": item["score"],
                }
            )
        
        result = build_model_result(
            "XLM-R", True,
            {
                "model_info": "XLM-RoBERTa (Facebook AI 2019)",
                "architecture": "RoBERTa for 100+ languages",
                "parameters": "270M",
                "training_data": "2.5TB of filtered CommonCrawl data",
                "task": "多语言掩码语言模型",
                "input": user_input,
                "cache_dir": cache_dir,
                "predictions": final_results,
                "note": "XLM-R 仅使用大规模单语预训练就达到了超越XLM（使用平行语料）的性能"
            },
            user_input=user_input,
            input_type="text"
        )
        save_json(result, output_dir / "latest_result.json")
        return result
        
    except Exception as e:
        result = build_model_result("XLM-R", False, str(e), user_input=user_input)
        save_json(result, output_dir / "latest_result.json")
        return result

if __name__ == "__main__":
    run_xlmr()
