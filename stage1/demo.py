import sys
from pathlib import Path

project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

from common.io_utils import save_json
from stage1.models.word2vec.run import run_word2vec
from stage1.models.elmo.run import run_elmo
from stage1.models.transformer.run import run_transformer
from stage1.models.bert.run import run_bert
from stage1.models.mbert.run import run_mbert

def run_demo(user_inputs: dict = None):
    """
    运行Stage 1的所有模型演示
    
    Args:
        user_inputs: 用户输入字典，示例：
        {
            "word2vec_word": "cat",
            "elmo_sent1": "i went to the bank",
            "elmo_sent2": "i sat on the river bank",
            "transformer_input": "The quick brown fox",
            "bert_input": "The capital of France is [MASK].",
            "mbert_input": "我们 去 [MASK] 玩。"
        }
    """
    output_dir = Path(__file__).parent / "outputs"
    output_dir.mkdir(parents=True, exist_ok=True)
    
    user_inputs = user_inputs or {}
    
    results = [
        run_word2vec(user_word=user_inputs.get("word2vec_word")),
        run_elmo(
            user_sentence_1=user_inputs.get("elmo_sent1"),
            user_sentence_2=user_inputs.get("elmo_sent2")
        ),
        run_transformer(user_input=user_inputs.get("transformer_input")),
        run_bert(user_input=user_inputs.get("bert_input")),
        run_mbert(user_input=user_inputs.get("mbert_input"))
    ]
    
    save_json({"stage": 1, "results": results}, output_dir / "latest_result.json")
    return results

if __name__ == "__main__":
    run_demo()
