from pathlib import Path
from typing import Any, Dict, List, Optional, Union

def get_project_root() -> Path:
    return Path(__file__).parent.parent

def build_model_result(
    model_name: str, 
    success: bool, 
    output: Union[str, dict],
    is_placeholder: bool = False,
    user_input: Optional[str] = None,
    input_type: Optional[str] = None
) -> dict:
    """
    构建模型运行结果对象
    
    Args:
        model_name: 模型名称
        success: 是否执行成功
        output: 模型输出结果
        is_placeholder: 是否仅为说明性占位
        user_input: 用户输入的内容（可选）
        input_type: 输入类型，如 'text', 'image_url' 等（可选）
    
    Returns:
        包含元数据的结果字典
    """
    result = {
        "model": model_name,
        "success": success,
        "is_placeholder": is_placeholder,
        "result": output,
    }
    
    if user_input is not None:
        result["user_input"] = user_input
        if input_type:
            result["input_type"] = input_type
    
    return result

# 常见的示例输入列表（用于 UI 提示）
# 设计原则：中文优先，支持多语言对照（中文、波斯语、阿拉伯语、英文、印地语等）
EXAMPLE_INPUTS = {
    "word2vec": [
        # 中文优先
        {"lang": "中文", "text": "狗"},
        {"lang": "中文", "text": "苹果"},
        {"lang": "中文", "text": "银行"},
        # 多语言对比
        {"lang": "波斯语", "text": "سگ"},
        {"lang": "英文", "text": "dog"},
        {"lang": "阿拉伯语", "text": "كلب"},
    ],
    "elmo": [
        {"lang": "中文", "text": "他去了银行存钱"},
        {"lang": "中文", "text": "我们在河岸边坐着"},
        {"lang": "英文", "text": "I went to the bank"},
        {"lang": "英文", "text": "We sat by the river bank"},
    ],
    "bert": [
        {"lang": "中文", "text": "中国的首都是[MASK]。"},
        {"lang": "中文", "text": "那是一个很[MASK]的城市。"},
        {"lang": "英文", "text": "The capital of France is [MASK]."},
        {"lang": "英文", "text": "[MASK] is a beautiful city."},
    ],
    "mbert": [
        {"lang": "中文", "text": "我们 去 [MASK] 玩。"},
        {"lang": "波斯语", "text": "ما برای بازی به [MASK] می رویم."},
        {"lang": "英文", "text": "We are going to [MASK]."},
        {"lang": "西班牙语", "text": "Vamos a [MASK] mañana."},
    ],
    "xlm": [
        # 跨语言相似度：中文优先格式
        {"lang": "中英对比", "text": "今天天气很好 | Today is a beautiful day"},
        {"lang": "中文+波斯", "text": "我喜欢阅读 | من کتاب خواندن را دوست دارم"},
        {"lang": "其他语言", "text": "hello world | 你好 世界"},
    ],
    "unicoder": [
        {"lang": "多语言编码", "text": "[CLS] 你好 [MASK] [SEP]"},
        {"lang": "多语言编码", "text": "[CLS] hello [MASK] [SEP]"},
        {"lang": "说明", "text": "此模型无开源版本，建议使用 XLM-R"},
    ],
    "xlmr": [
        {"lang": "中文", "text": "今天是一个很<mask>的日子。"},
        {"lang": "波斯语", "text": "امروز یک روز بسیار <mask> است."},
        {"lang": "英文", "text": "It is a very <mask> day."},
        {"lang": "阿拉伯语", "text": "هذا يوم جميل جدا <mask>."},
    ],
    "mbart": [
        {"lang": "中文->英文", "text": "translate Chinese to English: 你好，世界"},
        {"lang": "中文->法文", "text": "translate Chinese to French: 早上好"},
        {"lang": "英文->中文", "text": "translate English to Chinese: Good morning"},
    ],
    "mt5": [
        {"lang": "中文翻译", "text": "translate English to Chinese: Hello world"},
        {"lang": "中文总结", "text": "summarize: 机器学习是人工智能的一个分支..."},
        {"lang": "英文翻译", "text": "translate English to French: Good morning"},
    ],
    "bloom": [
        {"lang": "中文生成", "text": "今天天气很好，我想"},
        {"lang": "中文生成", "text": "人工智能的未来是"},
        {"lang": "英文生成", "text": "The future of technology is"},
        {"lang": "法文生成", "text": "Bonjour, je suis"},
    ],
    "xglm": [
        {"lang": "中文生成", "text": "今天天气很好，我想"},
        {"lang": "波斯语生成", "text": "روز خوبی است که"},
        {"lang": "英文生成", "text": "Hello, today is"},
    ],
    "gpt3": [
        {"lang": "中文问答", "text": "中国的首都是哪里?"},
        {"lang": "中文总结", "text": "总结这句话的意思: 机器学习是人工智能的分支"},
        {"lang": "英文问答", "text": "What is the capital of France?"},
    ],
    "palm": [
        {"lang": "说明", "text": "PaLM 需要 Google API 密钥。无开源版本。"},
        {"lang": "建议", "text": "推荐使用: BLOOM, XGLM 或 Qwen"},
    ],
    "qwen": [
        {"lang": "中文", "text": "你好，请用一句话介绍你自己。"},
        {"lang": "中文", "text": "如何学习机器学习？"},
        {"lang": "中文", "text": "请列出5个AI应用场景"},
        {"lang": "英文", "text": "What is artificial intelligence?"},
    ],
    "llama": [
        {"lang": "中文", "text": "请解释什么是深度学习"},
        {"lang": "中文", "text": "写一个关于春天的短诗"},
        {"lang": "英文", "text": "What is deep learning?"},
        {"lang": "英文", "text": "Write a short poem about spring"},
    ],
    "nllb": [
        {"lang": "中文->英文", "text": "Good morning"},
        {"lang": "中文->波斯", "text": "这家公司在2024年售出了12540件产品"},
        {"lang": "中文->法文", "text": "你好，世界"},
    ],
    "madlad": [
        {"lang": "中文->多语言", "text": "巴拉克·奥巴马于七月访问了巴黎"},
        {"lang": "多语言翻译", "text": "请翻译到200种语言"},
    ],
    "aya": [
        {"lang": "中文对话", "text": "你最喜欢的编程语言是什么？"},
        {"lang": "中文对话", "text": "请用简单的语言解释量子计算"},
        {"lang": "英文对话", "text": "What is your favorite programming language?"},
    ],
}
