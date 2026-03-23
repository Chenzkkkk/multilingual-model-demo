#!/usr/bin/env python3
"""
快速生成所有Stage 3 & 4 的模型文件的脚本
"""
import sys
from pathlib import Path

# 定义所有需要创建的模型
MODELS = {
    "stage3": {
        "mbart": "mBART - 多语言翻译",
        "mt5": "mT5 - 序列到序列",
        "bloom": "BLOOM - 生成模型",
        "xglm": "XGLM - 跨语言生成",
        "gpt3": "GPT-3 (API)",
        "palm": "PaLM - Google模型"
    },
    "stage4": {
        "qwen1": "Qwen 1.0",
        "qwen2": "Qwen 2.0",
        "qwen3": "Qwen 3.0",
        "qwen_mt": "Qwen Multilingual",
        "llama4": "LLaMA 4",
        "nllb": "NLLB - No Language Left Behind",
        "madlad400": "MADLAD-400",
        "aya": "Aya - 多语言助手"
    }
}

TEMPLATE = '''import sys
from pathlib import Path
project_root = Path(__file__).parent.parent.parent.parent
sys.path.append(str(project_root))
from common.io_utils import save_json
from common.utils import build_model_result

def run_{model_func}(user_input: str = None):
    """
    {model_name} 模型演示
    """
    output_dir = Path(__file__).parent / "outputs"
    output_dir.mkdir(parents=True, exist_ok=True)
    
    try:
        if not user_input:
            user_input = "{default_input}"
        
        result = build_model_result(
            "{model_name}", True,
            {{
                "model_info": "{model_name}",
                "user_input": user_input,
                "status": "演示模型已加载"
            }},
            is_placeholder=True,
            user_input=user_input,
            input_type="text"
        )
        save_json(result, output_dir / "latest_result.json")
        return result
    except Exception as e:
        result = build_model_result("{model_name}", False, str(e), user_input=user_input)
        save_json(result, output_dir / "latest_result.json")
        return result

if __name__ == "__main__":
    run_{model_func}()
'''

def create_models():
    """创建所有模型文件"""
    # 使用绝对路径获取项目根目录
    try:
        project_root = Path(__file__).parent.absolute()
    except:
        project_root = Path(".").absolute()
    
    print(f"项目根目录: {project_root}")
    
    for stage, models in MODELS.items():
        stage_path = project_root / stage / "models"
        print(f"\n处理 {stage}: {stage_path}")
        
        for model_key, model_name in models.items():
            model_path = stage_path / model_key
            model_path.mkdir(parents=True, exist_ok=True)
            
            run_py = model_path / "run.py"
            
            # 跳过已存在的文件
            if run_py.exists():
                print(f"  ✓ {model_key} 已存在")
                continue
            
            # 生成默认输入
            default_input = "演示输入"
            if "mask" in model_key.lower():
                default_input = "这是一个 [MASK] 句子。"
            elif model_key in ["mt5", "nllb", "madlad400"]:
                default_input = "translate English to Chinese: Hello"
            elif model_key in ["qwen1", "qwen2", "qwen3"]:
                default_input = "你好"
            elif "llama" in model_key.lower():
                default_input = "Hello"
            
            # 生成run.py内容
            content = TEMPLATE.format(
                model_func=model_key.replace("-", "_"),
                model_name=model_name,
                default_input=default_input
            )
            
            with open(run_py, 'w', encoding='utf-8') as f:
                f.write(content)
            
            print(f"  ✓ 创建 {model_key}")
    
    print("\n✅ 所有模型文件创建完成！")

if __name__ == "__main__":
    create_models()
