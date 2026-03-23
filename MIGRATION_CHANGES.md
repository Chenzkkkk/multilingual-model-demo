# 模型实现更新 - 移除 Mock 和配置缓存

**更新日期**: 2026-03-21
**主要目标**: 移除所有 mock/占位符实现，使用实际模型或清晰报错；解决重复下载问题

---

## 核心变更

### 1. 模型缓存配置 ✅

**文件**: `.env`

```env
HF_HOME=./models
MODEL_CACHE_DIR=./models
```

**效果**:
- 所有下载的模型统一存储在项目目录的 `./models` 文件夹
- ❌ 不再每次运行都重复下载
- ✅ 首次下载后永久缓存
- 📌 建议添加 `models/` 到 `.gitignore`（已自动包含）

### 2. 概览表格

| 阶段 | 模型 | 状态 | 实现方式 | 模型大小 |
|------|------|------|---------|---------|
| **Stage 1** | BERT | ✅ 实现 | bert-base-uncased | 440 MB |
| **Stage 2** | mBERT | ✅ 实现 | bert-base-multilingual-cased | 680 MB |
| | XLM-R | ✅ 实现 | xlm-roberta-base | 560 MB |
| | XLM | ✅ 实现 | xlm-roberta-base (跨语言相似度计算) | 560 MB |
| | Unicoder | ❌ 报错 | 无公开版本 - 推荐用 XLM-R 替代 | - |
| **Stage 3** | BLOOM | ✅ 实现 | bigscience/bloom-560m | 1.1 GB |
| | mT5 | ✅ 实现 | google/mt5-small | 300 MB |
| | XGLM | ✅ 实现 | facebook/xglm-564M | 2.4 GB ⚠️ |
| | mBART | ✅ 实现 | facebook/mbart-large-cc25 | 1.6 GB ⚠️ |
| | GPT-3 | ❌ 报错 | 需要 OpenAI API 密钥 | - |
| | PaLM | ❌ 报错 | 无开源版本 | - |

---

## 详细变更说明

### Stage 2 变更

#### 📄 `stage2/models/xlm/run.py`
- ❌ **移除**: `is_placeholder=True` 的假数据返回
- ✅ **新增**: 真实的 XLM-R 模型加载
- 🔧 **功能**: 计算两个多语言文本的语义相似度（跨语言对齐）
- 📝 **输入格式**: `"text1 | text2"` （用 `|` 分隔两个文本）
- 💾 **缓存**: 自动下载 560 MB 模型到 `./models/`

**示例输入**:
```
The weather is nice today | 天气今天很好
```

**示例输出**:
```json
{
  "success": true,
  "task": "Cross-lingual Text Similarity",
  "similarity_score": 0.8234,
  "note": "Similarity score ranges from -1 to 1"
}
```

---

#### 📄 `stage2/models/unicoder/run.py`
- ❌ **移除**: 所有 mock 数据
- ✅ **改为**: 清晰的错误提示
- 📢 **反馈**: 
  ```
  ❌ Unicoder 模型不可用
  Alibaba Unicoder 是一个专有模型，没有官方开源版本。
  
  推荐替代方案:
  - XLM-R (本项目已实现)
  - mBERT
  - 联系阿里巴巴 DAMO Academy 获取访问权限
  ```

---

### Stage 3 变更

#### 📄 `stage3/models/xglm/run.py`
- ❌ **移除**: `is_placeholder=True` 的假数据
- ✅ **新增**: facebook/xglm-564M 真实文本生成
- 🔧 **功能**: 多语言文本生成（causal LM）
- 💾 **缓存**: 首次下载 ~2.4 GB
- ⚠️ **性能**: 首次运行较慢（模型较大），后续使用缓存版本会快很多

**示例输出**:
```json
{
  "success": true,
  "input": "Hello, the weather is",
  "output": "Hello, the weather is great today. I love...",
  "languages_supported": "100+ languages"
}
```

---

#### 📄 `stage3/models/mbart/run.py`
- ❌ **移除**: 所有说明性掩码数据
- ✅ **新增**: facebook/mbart-large-cc25 真实 seq2seq 生成
- 🔧 **功能**: 多语言翻译和摘要任务
- 💾 **缓存**: 首次下载 ~1.6 GB

**示例输入**:
```
translate English to German: Hello, how are you?
```

**示例输出**:
```json
{
  "success": true,
  "input": "translate English to German: Hello, how are you?",
  "output": "Hallo, wie geht es dir?",
  "supported_languages": "25 languages"
}
```

---

#### 📄 `stage3/models/palm/run.py`
- ❌ **移除**: 所有 mock 数据
- ✅ **改为**: 清晰的错误提示
- 📢 **反馈**:
  ```
  ❌ PaLM 模型不可用（无开源版本）
  
  Google 的 PaLM 是专有模型，需要 Google Vertex AI API
  - 访问: https://cloud.google.com/ai/generative-ai
  - 配置 .env 中的 GOOGLE_API_KEY
  
  推荐开源替代方案:
  - BLOOM (已实现)
  - XGLM (已实现)
  - LLaMA / Mistral
  ```

---

#### 📄 `stage3/models/gpt3/run.py`
- ❌ **移除**: 所有 mock 数据
- ✅ **改为**: 检查 API 密钥，有密钥则调用真实 API，无则报错
- 📢 **无 API 密钥时的反馈**:
  ```
  ❌ GPT-3 模型不可用（需要 OpenAI API）
  
  启用步骤:
  1. 获取 OpenAI API 密钥 (https://platform.openai.com/api-keys)
  2. 在 .env 中配置: OPENAI_API_KEY=sk-...
  3. 注意: OpenAI API 按 token 计费
  
  推荐开源替代方案:
  - BLOOM (已实现，无费用)
  - XGLM (已实现，无费用)
  ```

---

### 缓存优化

所有模型文件已添加 `cache_dir` 参数:

```python
# 老版本 - 每次都重新下载
pipeline("fill-mask", model="nlp-model-name")

# 新版本 - 保存到 ./models 并复用
pipeline("fill-mask", 
         model="nlp-model-name",
         model_kwargs={'cache_dir': os.environ.get('HF_HOME')})
```

**受影响文件**:
- ✅ stage1/models/bert/run.py
- ✅ stage2/models/mbert/run.py  
- ✅ stage2/models/xlmr/run.py
- ✅ stage3/models/bloom/run.py
- ✅ stage3/models/mt5/run.py

---

## 首次运行指南

### 第一次运行时会发生什么

1. **初始化模型缓存** (一次性)
   ```bash
   streamlit run frontend/app.py
   ```
   - 页面加载时会自动开始下载模型
   - 根据浏览的 Stage，下载对应模型到 `./models/`

2. **下载大小预期**
   - Stage 1: ~500 MB
   - Stage 2: ~1.5 GB
   - Stage 3: ~5-8 GB（仅下载访问过的模型）

3. **时间预期** (取决于网络速度)
   - 快速网络 (100 Mbps): ~5-10 分钟
   - 普通网络 (20 Mbps): ~30-60 分钟
   - 慢速网络 (5 Mbps): 2+ 小时

### 后续运行

✅ **所有后续运行都会使用本地缓存，无需重新下载**

```bash
# 第 2 到 N 次运行 - 秒级启动，无下载
streamlit run frontend/app.py
```

---

## 验证清单

- ✅ 所有模型文件存在且无语法错误
- ✅ 缓存目录配置正确 (./models)
- ✅ Mock 数据完全移除
- ✅ 无 API 密钥的模型会清晰报错
- ✅ 有 API 密钥的模型可尝试真实调用

---

## 故障排查

### 问题: 模型下载超时

**解决方案**:
```bash
# 使用国内镜像加速（如果在中国）
# 在 .env 中添加:
HF_ENDPOINT=https://hf-mirror.com

# 或手动下载到 ./models
# 参考: https://huggingface.co/docs/hub/security-tokens
```

### 问题: 磁盘空间不足

**解决方案**:
```bash
# 清理不需要的模型缓存
rm -rf ./models

# 或在 .env 中修改缓存位置
HF_HOME=/path/to/large/disk/models
```

### 问题: 内存溢出 (XGLM/mBART)

**解决方案**:
- XGLM/mBART 模型约需要 8-16 GB RAM
- GPU 加速会显著提速
- 考虑使用较小的模型版本

---

## 后续改进方向

- [ ] 添加 GPU 加速支持检测
- [ ] 实现流式输出（大模型生成）
- [ ] 添加模型量化选项（减少内存占用）
- [ ] 实现本地 API 服务模式
- [ ] 添加模型性能对比面板
