from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Any, Dict, List

from common.benchmark_utils import get_example_by_language, load_benchmarks
from stage1.models.bert.run import run_bert
from stage1.models.elmo.run import run_elmo
from stage1.models.mbert.run import run_mbert
from stage1.models.transformer.run import run_transformer
from stage1.models.word2vec.run import run_word2vec
from stage2.models.xlm.run import run_xlm
from stage2.models.xlmr.run import run_xlmr
from stage3.models.bloom.run import run_bloom
from stage3.models.mbart.run import run_mbart
from stage3.models.mt5.run import run_mt5
from stage3.models.xglm.run import run_xglm
from stage4.models.aya.run import run_aya
from stage4.models.llama4.run import run_llama4
from stage4.models.madlad400.run import run_madlad400
from stage4.models.nllb.run import run_nllb
from stage4.models.qwen1.run import run_qwen1
from stage4.models.qwen2.run import run_qwen2
from stage4.models.qwen3.run import run_qwen3
from stage4.models.qwen_mt.run import run_qwen_mt

TASK_MODEL_OPTIONS: Dict[str, List[str]] = {
    "stage1_mask_filling": ["bert", "mbert"],
    "stage1_word_sense": ["word2vec", "elmo", "transformer"],
    "xnli": ["qwen2", "qwen3", "qwen1", "llama4", "aya"],
    "mgsm": ["qwen2", "qwen3", "qwen1", "llama4", "aya"],
    "xquad": ["qwen2", "qwen3", "qwen1", "llama4", "aya"],
    "belebele": ["qwen2", "qwen3", "qwen1", "llama4", "aya"],
    "flores_200": ["nllb", "madlad400", "qwen_mt", "qwen2", "qwen3"],
}

MODEL_LABELS: Dict[str, str] = {
    "word2vec": "Word2Vec",
    "elmo": "ELMo",
    "transformer": "Transformer",
    "bert": "BERT",
    "mbert": "mBERT",
    "xlm": "XLM",
    "xlmr": "XLM-R",
    "mbart": "mBART",
    "mt5": "mT5",
    "bloom": "BLOOM",
    "xglm": "XGLM",
    "qwen1": "Qwen1",
    "qwen2": "Qwen2",
    "qwen3": "Qwen3",
    "llama4": "LLaMA4",
    "aya": "Aya",
    "nllb": "NLLB",
    "madlad400": "MADLAD-400",
    "qwen_mt": "Qwen-MT",
}

LANG_TO_EN = {
    "中文": "Chinese",
    "英文": "English",
    "英语": "English",
    "波斯语": "Persian",
    "阿拉伯语": "Arabic",
    "法语": "French",
    "法文": "French",
    "德语": "German",
    "德文": "German",
    "西班牙语": "Spanish",
    "日语": "Japanese",
    "韩语": "Korean",
    "俄语": "Russian",
}


@dataclass
class EvalItem:
    case_id: str
    case_type: str
    language: str
    prompt: str
    model_output: str
    expected: str
    score: float
    is_correct: bool


def _extract_output_text(model_result: Dict[str, Any]) -> str:
    payload = model_result.get("result")
    if isinstance(payload, str):
        return payload
    if not isinstance(payload, dict):
        return str(payload)

    output = payload.get("output")
    if isinstance(output, str) and output.strip():
        return output.strip()

    preds = payload.get("predictions")
    if isinstance(preds, list) and preds:
        lines = []
        for item in preds[:5]:
            if isinstance(item, dict):
                token = item.get("token") or item.get("label") or item.get("word")
                if token:
                    lines.append(str(token))
        if lines:
            return "\n".join(lines)

    return str(payload)


def _normalize_label(text: str) -> str:
    t = (text or "").strip().lower()
    if any(k in t for k in ["contradiction", "矛盾", "تناقض", "متناقض"]):
        return "contradiction"
    if any(k in t for k in ["entailment", "蕴含", "دلالة", "نتیجه"]):
        return "entailment"
    if any(k in t for k in ["neutral", "中立", "محايد", "بی\u200cطرف"]):
        return "neutral"
    return "unknown"


def _first_number(text: str) -> str:
    m = re.search(r"-?\d+(?:\.\d+)?", text or "")
    return m.group(0) if m else ""


def _char_f1(pred: str, ref: str) -> float:
    p = list((pred or "").replace(" ", ""))
    r = list((ref or "").replace(" ", ""))
    if not p or not r:
        return 0.0

    from collections import Counter

    cp = Counter(p)
    cr = Counter(r)
    overlap = 0
    for k in cp:
        overlap += min(cp[k], cr.get(k, 0))

    precision = overlap / len(p)
    recall = overlap / len(r)
    if precision + recall == 0:
        return 0.0
    return 2 * precision * recall / (precision + recall)


def _invoke_model(model_key: str, prompt: str, task_name: str, target_lang: str = "English") -> Dict[str, Any]:
    if model_key == "word2vec":
        return run_word2vec(user_word=(prompt or "").strip().split(" ")[0] if (prompt or "").strip() else None)
    if model_key == "elmo":
        text = (prompt or "").strip()
        if "|" in text:
            p1, p2 = text.split("|", 1)
            return run_elmo(user_sentence_1=p1.strip(), user_sentence_2=p2.strip())
        return run_elmo(user_sentence_1=text, user_sentence_2=text)
    if model_key == "transformer":
        return run_transformer(user_input=prompt)
    if model_key == "bert":
        return run_bert(user_input=prompt)
    if model_key == "mbert":
        return run_mbert(user_input=prompt)
    if model_key == "xlm":
        return run_xlm(user_input=prompt)
    if model_key == "xlmr":
        xlmr_prompt = prompt if "<mask>" in (prompt or "") else f"{prompt} <mask>"
        return run_xlmr(user_input=xlmr_prompt)
    if model_key == "mbart":
        return run_mbart(user_input=prompt)
    if model_key == "mt5":
        return run_mt5(user_input=prompt)
    if model_key == "bloom":
        return run_bloom(user_input=prompt)
    if model_key == "xglm":
        return run_xglm(user_input=prompt)
    if model_key == "qwen1":
        return run_qwen1(user_input=prompt)
    if model_key == "qwen2":
        return run_qwen2(user_input=prompt)
    if model_key == "qwen3":
        return run_qwen3(user_input=prompt)
    if model_key == "llama4":
        return run_llama4(user_input=prompt)
    if model_key == "aya":
        return run_aya(user_input=prompt)
    if model_key == "nllb":
        return run_nllb(user_input=f"translate Chinese to {target_lang}: {prompt}")
    if model_key == "madlad400":
        return run_madlad400(user_input=f"translate Chinese to {target_lang}: {prompt}")
    if model_key == "qwen_mt":
        return run_qwen_mt(
            user_input=prompt,
            source_lang="Chinese",
            target_lang=target_lang,
            domains="General",
        )
    raise ValueError(f"Unsupported model: {model_key}")


def _build_prompt(task_name: str, example: Dict[str, Any]) -> str:
    if task_name == "stage1_mask_filling":
        return str(example.get("text", ""))
    if task_name == "stage1_word_sense":
        sents = example.get("sentences", [])
        if isinstance(sents, list) and len(sents) >= 2:
            return f"{sents[0]} | {sents[1]}"
        return str(example.get("word", "bank"))
    if task_name == "xnli":
        return (
            "请做自然语言推理任务。只输出一个标签：entailment / contradiction / neutral。\n"
            f"前提: {example.get('premise', '')}\n"
            f"假设: {example.get('hypothesis', '')}"
        )
    if task_name == "mgsm":
        return (
            "请解答以下数学题，并在最后一行只输出最终数字答案。\n"
            f"题目: {example.get('problem', '')}"
        )
    if task_name == "xquad":
        return (
            "请根据上下文回答问题，只输出简短答案短语。\n"
            f"上下文: {example.get('context', '')}\n"
            f"问题: {example.get('question', '')}"
        )
    if task_name == "belebele":
        options = example.get("options", [])
        option_block = "\n".join([f"{idx+1}. {opt}" for idx, opt in enumerate(options)])
        return (
            "请阅读文本并回答选择题。只输出一个选项内容，不要解释。\n"
            f"文本: {example.get('passage', '')}\n"
            f"问题: {example.get('question', '')}\n"
            f"选项:\n{option_block}"
        )
    if task_name == "flores_200":
        tgt = example.get("target_lang", "英文")
        return (
            f"请将以下中文句子翻译成{tgt}，只输出翻译结果，不要解释。\n"
            f"{example.get('source', '')}"
        )
    raise ValueError(f"Unsupported task: {task_name}")


def _evaluate(task_name: str, output_text: str, example: Dict[str, Any]) -> tuple[float, bool, str]:
    if task_name == "stage1_mask_filling":
        gold = str(example.get("expected", "")).strip().lower()
        out = str(output_text or "").strip().lower()
        ok = bool(gold) and (gold in out)
        return (1.0 if ok else 0.0), ok, example.get("expected", "")

    if task_name == "stage1_word_sense":
        # 该任务主要用于展示语境词义差异，采用可运行性与输出完整度作为演示评分。
        out = str(output_text or "").strip()
        ok = len(out) >= 6
        expected = "两句中同词的语义差异解释"
        return (1.0 if ok else 0.0), ok, expected

    if task_name == "xnli":
        pred = _normalize_label(output_text)
        gold = _normalize_label(example.get("label", ""))
        ok = pred == gold and gold != "unknown"
        return (1.0 if ok else 0.0), ok, gold

    if task_name == "mgsm":
        pred_num = _first_number(output_text)
        gold_num = _first_number(example.get("answer", ""))
        ok = bool(pred_num) and pred_num == gold_num
        return (1.0 if ok else 0.0), ok, example.get("answer", "")

    if task_name == "xquad":
        answers = example.get("answers", [])
        out = (output_text or "").lower()
        ok = any((ans or "").lower() in out for ans in answers)
        return (1.0 if ok else 0.0), ok, " / ".join(answers)

    if task_name == "belebele":
        gold = str(example.get("answer", "")).strip().lower()
        out = str(output_text).strip().lower()
        ok = gold and gold in out
        return (1.0 if ok else 0.0), ok, example.get("answer", "")

    if task_name == "flores_200":
        ref = str(example.get("target", ""))
        score = _char_f1(output_text, ref)
        ok = score >= 0.35
        return score, ok, ref

    return 0.0, False, ""


def run_benchmark(
    task_name: str,
    model_key: str,
    language: str,
    max_cases: int,
) -> Dict[str, Any]:
    benchmarks = load_benchmarks()
    cases = benchmarks.get(task_name, [])

    eval_items: List[EvalItem] = []
    success_calls = 0
    fail_calls = 0

    for case in cases[:max_cases]:
        case_id = case.get("id", "unknown")
        case_type = case.get("type", "")
        example = get_example_by_language(case, language)
        if not example:
            continue

        prompt = _build_prompt(task_name, example)

        target_lang_cn = str(example.get("target_lang", "英文"))
        target_lang_en = LANG_TO_EN.get(target_lang_cn, "English")

        model_result = _invoke_model(
            model_key=model_key,
            prompt=example.get("source", "") if task_name == "flores_200" else prompt,
            task_name=task_name,
            target_lang=target_lang_en,
        )
        if model_result.get("success"):
            success_calls += 1
        else:
            fail_calls += 1

        output_text = _extract_output_text(model_result)
        score, is_correct, expected = _evaluate(task_name, output_text, example)

        eval_items.append(
            EvalItem(
                case_id=case_id,
                case_type=case_type,
                language=language,
                prompt=prompt,
                model_output=output_text,
                expected=expected,
                score=score,
                is_correct=is_correct,
            )
        )

    if not eval_items:
        return {
            "task_name": task_name,
            "model_key": model_key,
            "model_label": MODEL_LABELS.get(model_key, model_key),
            "language": language,
            "num_cases": 0,
            "call_success": success_calls,
            "call_failed": fail_calls,
            "metric_name": "accuracy",
            "metric_value": 0.0,
            "items": [],
        }

    if task_name == "flores_200":
        metric_name = "char_f1"
        metric_value = sum(i.score for i in eval_items) / len(eval_items)
    else:
        metric_name = "accuracy"
        metric_value = sum(1 for i in eval_items if i.is_correct) / len(eval_items)

    return {
        "task_name": task_name,
        "model_key": model_key,
        "model_label": MODEL_LABELS.get(model_key, model_key),
        "language": language,
        "num_cases": len(eval_items),
        "call_success": success_calls,
        "call_failed": fail_calls,
        "metric_name": metric_name,
        "metric_value": metric_value,
        "items": [
            {
                "case_id": i.case_id,
                "case_type": i.case_type,
                "language": i.language,
                "prompt": i.prompt,
                "model_output": i.model_output,
                "expected": i.expected,
                "score": i.score,
                "is_correct": i.is_correct,
            }
            for i in eval_items
        ],
    }
