import sys
from pathlib import Path

project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

from common.io_utils import save_json
from common.utils import build_model_result


LANG_KEY_TO_API_NAME = {
    "chinese": "Chinese",
    "english": "English",
    "persian": "Persian",
    "french": "French",
    "arabic": "Arabic",
    "hindi": "Hindi",
    "spanish": "Spanish",
    "russian": "Russian",
    "german": "German",
    "japanese": "Japanese",
    "korean": "Korean",
}

LANG_KEY_TO_ZH = {
    "chinese": "中文",
    "english": "英语",
    "persian": "波斯语",
    "french": "法语",
    "arabic": "阿拉伯语",
    "hindi": "印地语",
    "spanish": "西班牙语",
    "russian": "俄语",
    "german": "德语",
    "japanese": "日语",
    "korean": "韩语",
}


def _normalize_lang_keys(lang_values) -> list[str]:
    if not isinstance(lang_values, list):
        return []
    result: list[str] = []
    for item in lang_values:
        key = str(item).strip().lower()
        if key in LANG_KEY_TO_API_NAME and key not in result:
            result.append(key)
    return result


def _inject_answer_language_instruction(prompt: str, lang_keys: list[str]) -> str:
    if not prompt.strip() or not lang_keys:
        return prompt
    lang_zh = [LANG_KEY_TO_ZH[k] for k in lang_keys if k in LANG_KEY_TO_ZH]
    if not lang_zh:
        return prompt
    instruction = f"请使用以下语言作答（可分段输出）：{'、'.join(lang_zh)}。"
    return f"{prompt.strip()}\n\n{instruction}"

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
                    src_key = str(user_inputs.get("qwen_mt_source_lang") or "chinese").strip().lower()
                    target_keys = _normalize_lang_keys(user_inputs.get("qwen_mt_target_langs") or [])
                    if not target_keys:
                        target_keys = ["english"]
                    target_keys = [k for k in target_keys if k != src_key]
                    if not target_keys:
                        target_keys = ["english"]

                    collected_outputs: list[dict] = []
                    all_success = True
                    for target_key in target_keys:
                        single_result = run_func(
                            user_input=user_inputs.get("qwen_mt_input"),
                            source_lang=LANG_KEY_TO_API_NAME.get(src_key, "Chinese"),
                            target_lang=LANG_KEY_TO_API_NAME.get(target_key, "English"),
                            domains=user_inputs.get("qwen_mt_domains") or "General",
                        )
                        if not single_result.get("success"):
                            all_success = False
                        payload = single_result.get("result") if isinstance(single_result.get("result"), dict) else {}
                        text = ""
                        if isinstance(payload, dict):
                            text = str(payload.get("output") or "").strip()
                        collected_outputs.append(
                            {
                                "language": LANG_KEY_TO_ZH.get(target_key, target_key),
                                "language_code": target_key,
                                "text": text,
                            }
                        )

                    result = build_model_result(
                        "Qwen Multilingual",
                        all_success,
                        {
                            "input": user_inputs.get("qwen_mt_input") or "",
                            "source_lang": LANG_KEY_TO_ZH.get(src_key, src_key),
                            "translations": collected_outputs,
                            "output": "\n".join(f"{x['language']}: {x['text']}" for x in collected_outputs if x.get("text")),
                        },
                        is_placeholder=False,
                        user_input=user_inputs.get("qwen_mt_input") or "",
                        input_type="text",
                    )
                elif model == "nllb":
                    result = run_func(
                        user_input=user_inputs.get("nllb_input"),
                        target_languages=user_inputs.get("nllb_target_langs") or [],
                    )
                elif model == "madlad400":
                    result = run_func(
                        user_input=user_inputs.get("madlad400_input"),
                        target_languages=user_inputs.get("madlad400_target_langs") or [],
                    )
                elif model in {"qwen1", "qwen2", "qwen3", "llama4", "aya"}:
                    raw_prompt = user_inputs.get(f"{model}_input") or ""
                    lang_keys = _normalize_lang_keys(user_inputs.get(f"{model}_langs") or [])
                    prompt = _inject_answer_language_instruction(raw_prompt, lang_keys)
                    result = run_func(user_input=prompt)
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
