"""
Word2Vec - Static Word Embeddings
词向量模型演示（静态词表示）
"""
import sys
from pathlib import Path

project_root = Path(__file__).parent.parent.parent.parent
sys.path.append(str(project_root))

from common.io_utils import save_json
from common.utils import build_model_result

def run_word2vec(user_word: str = None, corpus_text: str = None):
    """
    Word2Vec 演示 - Skip-gram 模型
    用户输入：要查询的词 + 训练语料
    """
    output_dir = Path(__file__).parent / "outputs"
    output_dir.mkdir(parents=True, exist_ok=True)
    
    try:
        from gensim.models import Word2Vec
        
        # 默认语料库
        default_corpus = """
        the cat sat on the mat
        a dog played in the park
        the dog chased the cat
        birds fly in the sky
        the bird sang a song
        i deposited money in the bank yesterday
        we had a picnic on the river bank after rain
        the startup team discussed innovation strategy at night
        financial risk can spread quickly across the market
        medical researchers published a multilingual benchmark report
        """
        
        corpus = corpus_text or default_corpus
        
        # 分词
        sentences = [line.strip().split() for line in corpus.strip().split('\n') if line.strip()]
        
        # 如果句子太少，添加一些示例
        if len(sentences) < 3:
            default_sentences = [
                ["the", "cat", "sat", "on", "the", "mat"],
                ["a", "dog", "played", "in", "the", "park"],
                ["the", "dog", "chased", "the", "cat"],
                ["birds", "fly", "in", "the", "sky"],
            ]
            sentences = default_sentences
        
        # 训练Word2Vec模型
        model = Word2Vec(sentences=sentences, vector_size=10, window=3, min_count=1, workers=1, sg=1)
        
        # 默认查询词
        query_word = user_word or "cat"
        
        # 检查词是否在词汇表中
        query_word_lc = query_word.lower()
        if query_word_lc not in model.wv:
            available_words = list(model.wv.index_to_key)[:10]
            try:
                from difflib import get_close_matches

                suggestions = get_close_matches(query_word_lc, list(model.wv.index_to_key), n=3, cutoff=0.5)
            except Exception:
                suggestions = []
            suggestion_text = f"；你可能想查：{suggestions}" if suggestions else ""
            return build_model_result(
                "Word2Vec",
                False,
                f"词 '{query_word}' 不在语料库中。可用的词包括：{available_words}{suggestion_text}",
                user_input=f"query_word={user_word}, corpus_provided={corpus_text is not None}",
                input_type="text"
            )
        
        # 获取最相似的词
        similar_words = model.wv.most_similar(query_word_lc, topn=5)
        
        results = {
            "query_word": query_word,
            "embeddings": [
                {
                    "word": word,
                    "similarity_score": float(score)
                }
                for word, score in similar_words
            ],
            "vocab_size": len(model.wv)
        }
        
        result = build_model_result(
            "Word2Vec",
            True,
            {
                "model_info": "Word2Vec Skip-gram (Mikolov et al., 2013)",
                "embedding_type": "Static Word Embeddings",
                "user_input_word": query_word,
                "results": results
            },
            user_input=user_word or "cat",
            input_type="text"
        )
        
        save_json(result, output_dir / "latest_result.json")
        return result
        
    except Exception as e:
        result = build_model_result("Word2Vec", False, str(e), user_input=user_word or "cat")
        save_json(result, output_dir / "latest_result.json")
        return result

if __name__ == "__main__":
    run_word2vec()
