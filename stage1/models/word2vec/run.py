from gensim.models import Word2Vec
from pathlib import Path
import os
import sys

project_root = Path(__file__).parent.parent.parent.parent
sys.path.append(str(project_root))

from common.io_utils import save_json, load_json
from common.utils import build_model_result

def run_word2vec():
    output_dir = Path(__file__).parent / "outputs"
    output_dir.mkdir(parents=True, exist_ok=True)
    
    sentences = [
        "你好 世界".split(),
        "hello world".split(),
        "hola mundo".split(),
        "word embeddings are useful".split(),
        "词向量 是 有用 的".split()
    ]
    
    try:
        model = Word2Vec(sentences=sentences, vector_size=10, window=2, min_count=1, workers=1)
        similars = model.wv.most_similar("你好", topn=3)
        formatted_sims = [{"word": word, "score": float(score)} for word, score in similars]
        
        result = build_model_result("word2vec", True, {"query": "你好", "similar_words": formatted_sims})
        save_json(result, output_dir / "latest_result.json")
        return result
    except Exception as e:
        result = build_model_result("word2vec", False, str(e))
        save_json(result, output_dir / "latest_result.json")
        return result

if __name__ == "__main__":
    run_word2vec()
