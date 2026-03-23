"""
多语言 benchmark 工具函数
支持中文优先的多语言展示
"""
import json
from pathlib import Path
from typing import Dict, List, Optional, Any


def load_benchmarks() -> Dict[str, Any]:
    """加载 benchmark.json 文件"""
    benchmark_path = Path(__file__).parent / "benchmark.json"
    with open(benchmark_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def get_benchmark_by_id(benchmark_type: str, example_id: str) -> Optional[Dict]:
    """
    按 ID 获取单个 benchmark 案例
    """
    benchmarks = load_benchmarks()
    if benchmark_type in benchmarks:
        for item in benchmarks[benchmark_type]:
            if isinstance(item, dict) and item.get('id') == example_id:
                return item
    return None


def get_multilingual_versions(benchmark_item: Dict) -> List[str]:
    """
    提取 benchmark 中的所有语言版本
    
    返回带有中文优先的语言列表
    """
    languages = []
    
    # 对于有 examples 字段的新格式
    if 'examples' in benchmark_item:
        for example in benchmark_item['examples']:
            if 'lang' in example:
                languages.append(example['lang'])
    
    return languages


def get_example_by_language(benchmark_item: Dict, lang: str) -> Optional[Dict]:
    """
    按语言获取 benchmark 中的特定版本
    """
    if 'examples' in benchmark_item:
        for example in benchmark_item['examples']:
            if example.get('lang') == lang:
                return example
    return None


def get_default_language(benchmark_item: Dict) -> str:
    """
    获取默认展示语言（中文优先）
    """
    languages = get_multilingual_versions(benchmark_item)
    
    # 优先级：中文 > 其他语言 > 第一个
    if '中文' in languages:
        return '中文'
    if len(languages) > 0:
        return languages[0]
    return 'unknown'


def format_xnli_display(example: Dict) -> str:
    """
    格式化 XNLI 案例的展示
    """
    parts = [
        f"**语言**: {example.get('lang', '未知')}",
        f"",
        f"**前提 (Premise)**:",
        f"> {example.get('premise', '')}",
        f"",
        f"**假设 (Hypothesis)**:",
        f"> {example.get('hypothesis', '')}",
        f"",
        f"**正确标签**: {example.get('label', '')}",
        f"",
        f"**说明**: {example.get('label_text', '')}",
    ]
    return "\n".join(parts)


def format_mgsm_display(example: Dict) -> str:
    """
    格式化 MGSM 数学推理案例的展示
    """
    parts = [
        f"**语言**: {example.get('lang', '未知')}",
        f"",
        f"**问题**:",
        f"> {example.get('problem', '')}",
        f"",
        f"**答案**: {example.get('answer', '')}",
        f"",
        f"**推理**: {example.get('reasoning', '')}",
    ]
    return "\n".join(parts)


def format_flores_display(example: Dict) -> str:
    """
    格式化 FLORES 翻译案例的展示
    """
    parts = [
        f"**源语言**: {example.get('lang', '未知')}",
        f"",
        f"**源文本**:",
        f"> {example.get('source', '')}",
        f"",
        f"**目标语言**: {example.get('target_lang', '未知')}",
        f"",
        f"**翻译**:",
        f"> {example.get('target', '')}",
    ]
    return "\n".join(parts)


def format_xquad_display(example: Dict) -> str:
    """
    格式化 XQuAD 问答案例的展示
    """
    parts = [
        f"**语言**: {example.get('lang', '未知')}",
        f"",
        f"**上下文**:",
        f"> {example.get('context', '')}",
        f"",
        f"**问题**: {example.get('question', '')}",
        f"",
        f"**答案**: {', '.join(example.get('answers', []))}",
        f"",
        f"**抽取类型**: {example.get('expected_extraction', '')}",
    ]
    return "\n".join(parts)


def format_belebele_display(example: Dict) -> str:
    """
    格式化 BELEBELE 阅读理解案例的展示
    """
    parts = [
        f"**语言**: {example.get('lang', '未知')}",
        f"",
        f"**文本**:",
        f"> {example.get('passage', '')}",
        f"",
        f"**问题**: {example.get('question', '')}",
        f"",
        f"**选项**:",
    ]
    
    options = example.get('options', [])
    for i, opt in enumerate(options, 1):
        marker = "✅" if opt == example.get('answer') else "  "
        parts.append(f"{marker} {i}. {opt}")
    
    parts.append(f"")
    parts.append(f"**正确答案**: {example.get('answer', '')}")
    
    return "\n".join(parts)


# 页面说明文案生成器

LANGUAGE_DESIGN_EXPLANATION = """
## 📌 语言设计说明

本页采用**中文优先**的多语言展示策略，原因如下：

### 1️⃣ 为什么中文优先？
- **课堂易理解**: 你能快速理解题意，不需要翻译
- **直观对比**: 同一道题在不同语言下，更容易看出模型表现差异
- **针对受众**: 课堂观众主是中文语境

### 2️⃣ 为什么引入波斯语、阿拉伯语？
- **文字系统差异大**: 波斯语/阿拉伯语（从右向左）vs 中文/英文（从左向右），视觉冲击强
- **展示真正的跨语言能力**: 
  - 只看英文 → 容易误认为模型主要擅长英文
  - 加入波斯/阿拉伯 → 清楚地展示模型是否真的具备多语言迁移能力
- **检验泛化边界**: 模型在低资源语言上的表现往往反映其泛化能力上限

### 3️⃣ 语言选择优先级
1. **中文** - 主展示语言，课堂讲解用
2. **波斯语** - 重点对照语言（文字差异最大）
3. **阿拉伯语** - 补充对照（使用者众多）
4. **英文** - 国际对照（便于论文对标）
5. **印地语** - 低资源语言样本（检验模型边界）

### 4️⃣ 如何阅读多语言版本？
- 左侧语言切换器：中文默认在第一位
- 切换任何语言后，查看**同一道题**在该语言中的表现
- 对比输出：观察前缀、格式、错误率等变化

---

**核心理念**: 多语言展示不是为了炫耀"我支持100种语言"，而是为了在课堂上
**清晰、直观地演示跨语言模型是否真的跨语言**。
"""

BENCHMARK_OVERVIEW = """
## 📚 精选评测任务说明

### XNLI - 跨语言自然语言推理
- **任务**: 给定前提和假设，判断是否蕴含、矛盾或中立
- **为什么重要**: 考查逻辑推理能力，不只是语言表面匹配
- **难点**: 否定、数字、指代等陷阱在不同语言中的表现差异

### MGSM - 多语言Grade School Math
- **任务**: 解决小学数学应用题
- **为什么重要**: 考查推理链条，不只是随机记忆
- **难点**: 数字、单位、时间在多语言中的表达和理解

### FLORES-200 - 翻译质量
- **任务**: 在200种语言间進行高质量翻译
- **为什么重要**: 考查语言间的语义保留，不只是词汇对齐
- **难点**: 专名、习语、文化特异性在翻译中的处理

### XQuAD - 跨语言问答
- **任务**: 从给定文本中抽取答案来回答问题
- **为什么重要**: 考查精确信息抽取能力，不只是大意理解
- **难点**: 不同语言中的相似表述可能对应不同答案

### BELEBELE - 阅读理解
- **任务**: 选择符合文本的正确答案
- **为什么重要**: 考查细节理解和推理，不只是关键词匹配
- **难点**: 低资源语言中的歧义、文化背景差异

---

**如何看这些任务的多语言版本**:
1. 先读中文版本，快速理解题意
2. 再看波斯语/阿拉伯语版本，观察同一任务的不同语言编码
3. 预测该语言版本的难度 (比中文更难/更容易/差不多)
4. 最后看模型输出，验证你的预测是否准确
"""
