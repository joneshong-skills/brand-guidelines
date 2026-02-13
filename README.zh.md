[English](README.md) | [繁體中文](README.zh.md)

# brand-guidelines

一個 Claude Code 技能，將 Anthropic 官方品牌色彩、字型及視覺識別套用至任何產出物。
基於 [Anthropic 官方技能](https://github.com/anthropics/skills/tree/main/skills/brand-guidelines)，適配為本機使用。

## 說明

1. 提供 Anthropic 官方品牌色彩盤（深色、淺色、灰色、強調色）
2. 套用正確字型：標題用 Poppins、內文用 Lora
3. 自訂字型不可用時自動退回 Arial/Georgia
4. 非文字形狀循環使用強調色（橘、藍、綠）
5. 適用於簡報、文件、HTML 及其他視覺產出物

## 功能特色

- 完整的 Anthropic 品牌色彩定義
- 智慧字型套用與自動退回機制
- 支援簡報（PPTX）品牌風格化
- 形狀與圖表的強調色循環
- 跨系統色彩一致性

## 安裝

```bash
git clone https://github.com/joneshong-skills/brand-guidelines.git ~/.claude/skills/brand-guidelines
```

## 使用方式

安裝後，直接要求 Claude 套用品牌風格：

- *「套用 Anthropic 品牌規範到這份簡報」*
- *「用品牌色彩設計這份文件」*
- *「Apply brand styling to this page」*
- *「用 Anthropic 的視覺識別來設計」*

## 品牌色彩

| 名稱 | 色碼 | 用途 |
|------|------|------|
| 深色 | `#141413` | 主要文字、深色背景 |
| 淺色 | `#faf9f5` | 淺色背景、深色上的文字 |
| 中灰 | `#b0aea5` | 次要元素 |
| 淺灰 | `#e8e6dc` | 微妙背景 |
| 橘色 | `#d97757` | 主要強調色 |
| 藍色 | `#6a9bcc` | 次要強調色 |
| 綠色 | `#788c5d` | 第三強調色 |

## 專案結構

```
brand-guidelines/
├── SKILL.md         # 技能定義及品牌規格
├── LICENSE.txt      # Apache 2.0 授權
├── README.md        # 英文說明
├── README.zh.md     # 繁體中文說明（本檔案）
├── references/      # 參考資料
├── scripts/         # 輔助腳本
└── assets/          # 品牌素材
```

## 授權

Apache 2.0（來自 Anthropic）
