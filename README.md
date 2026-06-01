# Twessie Premium Swimwear - Daily Content Generator

## 项目概述

自动化内容生产管道，每天生成5组创意×10个SKU的高端独立杂志风格产品企划。

### 输出内容

- **面料与配色分析** - 3个高级面料方向
- **Midjourney 生图提示词** - 2个场景的专业提示词
- **品牌Slogan文案** - 独立、锋芒的核心主张

### 美学标准

- ✨ Nordic Minimalism meets South France Riviera
- 🎨 Matte, crisp, intelligent luxury
- ❌ 拒绝廉价暴露风、高饱和度词汇
- 🧠 ENTP sharp, zero-fluff tone

---

## 快速开始

### 1. 本地环境设置

```bash
git clone https://github.com/twesliu-rgb/twessie-swimwear-content-generator.git
cd twessie-swimwear-content-generator

# 创建虚拟环境
python3 -m venv venv
source venv/bin/activate  # macOS/Linux
# 或
venv\Scripts\activate  # Windows

# 安装依赖
pip install -r requirements.txt
```

### 2. 配置 API 密钥（可选）

创建 `.env` 文件（不要提交到 git）：

```env
# 可选：如果你有 Hugging Face 账户，获取 free inference API token
HUGGINGFACE_API_KEY=hf_xxxxxxxxxxxx

# 可选：如果你有免费 OpenAI API token
OPENAI_API_KEY=sk_xxxxxxxxxxxx
```

### 3. 手动运行脚本

```bash
python scripts/daily_content_generator.py
```

输出会保存到 `output/{date}/` 目录。

### 4. 自动化运行（GitHub Actions）

脚本会自动在每天上午 9 点（UTC）运行，结果自动提交到仓库。

---

## 输出文件结构

```
output/
├── 2026-06-01/
│   ├── group_001/
│   │   ├── metadata.json          # 创意组元数据
│   │   ├── sku_001.json
│   │   ├── sku_002.json
│   │   └── ... (10 SKUs)
│   ├── group_002/
│   └── ... (5 groups total)
└── 2026-06-02/
    └── ...
```

### 输出格式示例

```json
{
  "date": "2026-06-01",
  "group_id": "group_001",
  "sku": "TWESSIE_SG_001",
  "fabric_analysis": {
    "direction_1": {
      "name": "方向一：微褶皱高弹肌理（Crinkled Seersucker）",
      "spec": "采用立体微压褶皱工艺...",
      "color_palette": "Stone Gray & Chalk White"
    },
    "direction_2": { ... },
    "direction_3": { ... }
  },
  "midjourney_prompts": {
    "scene_1_nordic_minimalism": "An editorial fashion lookbook...",
    "scene_2_south_france_sunlight": "A premium fashion campaign..."
  },
  "shopify_slogan": "We don't design to be stared at. We design to stand apart.",
  "generated_at": "2026-06-01T09:00:00Z"
}
```

---

## 自定义配置

编辑 `config/brand_guidelines.json` 来调整：

- 品牌美学关键词
- 面料方向模板
- Midjourney 提示词基础框架
- Slogan 生成规则

---

## 工作原理

### 内容生成引擎

1. **面料分析** - 从预定义的高级面料库中随机组合 + 美学约束
2. **Midjourney 提示词** - 基于场景模板 + 随机光影/质感参数
3. **Slogan 文案** - 使用 LLM（Hugging Face 或 OpenAI）生成独立风格文案

所有输出都通过**品牌一致性验证器**检查，确保符合极简主义美学。

---

## 许可

MIT License - 自由使用和修改

---

## 支持

有问题？在 Issues 中提问或查看 GitHub Discussions。
