# 多语言预训练模型综述与演示系统

这是一个课程项目，展示多语言预训练模型从静态词向量到现有大语言模型的发展过程。

## 项目结构
- `common/`: 基础公共代码
- `frontend/`: 基于 Streamlit 的客户端页面
- `stage1/`: 从 word2vec 到 BERT——预训练范式的奠基
- `stage2/`: mBERT / XLM / XLM-R——多语言 Encoder 预训练时代
- `stage3/`: 从 mT5 到 BLOOM——多语言生成的双路线过渡期
- `stage4/`: GPT-4 之后——多语言 LLM 的对齐、涌现与前沿

## 安装说明

```bash
conda create -n multilingual python=3.11 -y
conda activate multilingual
```
```bash
pip install -r requirements.txt
```

## 配置说明
复制 `.env.example` 为 `.env` 并填写相关 API Key：
```bash
cp .env.example .env
```

## 运行前端页面
```bash
streamlit run frontend/app.py
```
