# 🎮 Nintendo Switch Online 全球价格���虫

> 自动抓取全球 Nintendo Switch Online ���阅价格，实时���率���换，���到最���宜的���阅地区

[![Python](https://img.shields.io/badge/Python-3.9+-blue)](https://www.python.org/)
[![Playwright](https://img.shields.io/badge/Playwright-Latest-green)](https://playwright.dev/)

**🌐 语言**: [English](README.md) | 中文

## ✨ 核心功能

| 功能 | ���明 |
|------|------|
| 🌍 **全球���格���取** | 自���抓��� 40+ ���国家/地���的 Nintendo Switch Online 价��� |
| 💱 **实���汇率转���** | 集成 OpenExchangeRates API，将���有价格转换为���民币 |
| 🏆 **���能排序���析** | 按价格排序，快速���到最便���的订阅���区 |
| ���� **浏览���自动化** | 使用 Playwright 处理���户端���染页面 |
| ���� **标准化数据** | ���一的 JSON 格式输���，���于分析和���比 |

## 🚀 快速开始

### ���置要求

- Python 3.9+
- 免费��� OpenExchangeRates API 密���

### ���装步���

```bash
# 1. 克隆项目
git clone <your-repo-url>
cd nintendo-switch-online-prices

# 2. 安装���赖
pip install -r requirements.txt
playwright install chromium

# 3. 配置 API 密���
cp .env.example .env
# 编��� .env 文件，添加���的 API_KEY

# 4. ���行���虫
python run.py
```

### 🔑 获��� API 密钥

1. 访问 [OpenExchangeRates](https://openexchangerates.org/)
2. 注册免费���户���每月 1000 ���免���请求）
3. 获取你的 API 密钥���添加��� `.env` 文件

## 📊 数���输出

### 主���文件

```
nintendo_prices.json              # 原���价格数据
nintendo_prices_cny_sorted.json   # 按人���币排序���数据
```

### TOP 10 最便宜示例

```
���� 最便宜��� TOP 10:
--------------------------------------------------------------------------------
 1. Argentina             | Family - 12 months              | ¥   18.50 (ARS 2500.0)
 2. Turkey                | Family - 12 months              | ¥   32.80 (TRY 450.0)
 3. Brazil                | Individual - 12 months          | ��   45.20 (BRL 35.0)
 4. Russia                | Family - 12 months              | ¥   52.30 (RUB 1800.0)
 5. India                 | Individual - 12 months          | ¥   58.40 (INR 500.0)
```

## 🌍 支持的国���/地区

### ���洲 (9个)
日本���韩国、香港���新加���、马来���亚、泰���、印度尼西亚、菲���宾、台���

### 北美 (3个)
美���、加拿���、���西哥

### 欧洲 (20���)
���国���德国���法国���西班���、意大���、���兰���比利时���奥���利、���士���瑞典、挪威���丹麦、芬兰���波兰、捷克、葡萄���、俄罗斯���

### 大洋��� (2个)
澳大利���、新西���

### 南美 (5个)
巴���、阿根���、���利、哥伦比亚、���鲁

### 非洲 (1个)
南非

## 🛠️ ���用���法

### 方式一：���速运行（推荐）

```bash
python run.py
```

���会自动运���爬���和汇率���换，���显��� TOP 10 最便宜的订���。

### 方式二：分步���行

```bash
# 步骤 1: 运行爬虫
python nintendo.py

# 步骤 2: 转换���率并排序
python nintendo_rate_converter.py
```

### 方式���：���试模式

```bash
# 快速测���几个国家
python test_scraper.py
```

## 📁 ���目结构

```
nintendo-switch-online-prices/
├── nintendo.py                      # 主爬虫���本
├── nintendo_rate_converter.py       # 汇率转换���
���── run.py                           # 快速运行脚本
├── test_scraper.py                  # 测���脚本
├���─ requirements.txt                 # Python 依赖
���── .env.example                     # ���境变量模板
├── .gitignore                       # Git 忽略文件
���── README.md                        # 英文文档
���── README_zh.md                     # 中文���档
���── .github/workflows/
│   ���── weekly-scraper.yml          # GitHub Actions 自���化
├── nintendo_prices.json            # 原始数据（运行后生成）
└── nintendo_prices_cny_sorted.json # 排���数���（���行后生成）
```

## 🤖 GitHub Actions 自���化

项目包含 GitHub Actions 工���流���可以每周自动运行爬虫并更���数据。

### 设置步骤

1. Fork ���个项目���你的 GitHub
2. ���入 **Settings** → **Secrets and variables** → **Actions**
3. ���加 Secret：`API_KEY` = 你��� OpenExchangeRates API ���钥
4. 工作流���在每���日自���运行

## 🔧 ���术栈

| 技术 | 用途 | 版本 |
|------|------|------|
| Python | 核心���发语言 | 3.9+ |
| Playwright | ���览器自动化 | Latest |
| BeautifulSoup | HTML 解析 | 4.11.0+ |
| OpenExchangeRates API | 实时汇���数据 | v6 |

## 💡 使用建议

### 订���便���地区的注意���项

1. **账号地区设置**: 需要��� Nintendo 账号地区改为���标国���
2. **���付方式**: ���些���区可能需���当地支付方式
3. **IP 地址**: 可能需要���应地���的 IP 才能购买
4. **服务限制**: 不���地���的服务内容可能有���异

### 价格对比技巧

- 关注 **Family Plan 12个月** ���餐，通���最划算
- 考虑与朋友分摊 Family Plan ���用
- 定期查���价格���化，汇���波动可能影响���际���格

## ⚠️ 免���声明

- 本项���仅用于���习和研究目���
- 价格���据仅供参���，实���价格以官方为准
- 请���守 Nintendo 的服务���款
- 跨���购买可���存在风险，请谨���决定

## 🤝 ���献

���迎提交 Issue ��� Pull Request！

1. Fork ���项目
2. ���建特���分支：`git checkout -b feature/new-feature`
3. 提交更改���`git commit -m 'feat: add new feature'`
4. 推送分支���`git push origin feature/new-feature`
5. 提交 Pull Request

## 📝 更新���志

### v1.0.0 (2026-08-12)

- 🎉 ���始���本发布
- ✅ 支持 40+ 个国家/地���
- ��� Playwright 浏览器���动化
- ��� 实时汇���转换
- ✅ TOP 10 ���格排行
- ✅ GitHub Actions ���动化

## 📄 许���证

本���目仅用于学习���研究目的。请遵守相关法律和网���服务���款���

## ���� 致谢

本项目参���了以下优秀项目���

- [spotify-prices](https://github.com/SzeMeng76/spotify-prices) - Spotify ���球���格爬���
- [disneyplus-prices](https://github.com/SzeMeng76/disneyplus-prices) - Disney+ 全���价格爬虫

---

<div align="center">

**🎮 ���到���划算的 Nintendo Switch Online 订���！**

Made with ❤��� for Nintendo fans

[���始使���](#-快���开始) • [查���数据](#-数据输出) • [技术栈](#-技术栈)

</div>
