# 🎮 Nintendo Switch Online 全���价格爬虫

> 自动���取全球 Nintendo Switch Online ���阅价���，实时汇���转���，找到���便宜的订���地区

[![Python](https://img.shields.io/badge/Python-3.9+-blue)](https://www.python.org/)
[![Playwright](https://img.shields.io/badge/Playwright-Latest-green)](https://playwright.dev/)

## ✨ 功能特性

| 功能 | 描述 |
|------|-------------|
| 🌍 **���球价���抓取** | ���动抓取 40+ 个国家/地区的 Nintendo Switch Online 价格 |
| 💱 **实时汇率转换** | 集成 OpenExchangeRates API，将所有价格转换为���民币 |
| 🏆 **智能排序分析** | 按价���排序���快速找���最便宜的订阅地区 |
| 🤖 **���览器���动���** | 使用 Playwright 处���客户端渲染页��� |
| ���� **标���化���据** | ���一的 JSON 格式输出，���于分析 |

## 🚀 ���速开���

### 1. 克隆���目

```bash
git clone <your-repo-url>
cd nintendo-switch-online-prices
```

### 2. 安装���赖

```bash
pip install -r requirements.txt
playwright install chromium
```

### 3. 配��� API 密钥

```bash
# 复���环境���量���板
cp .env.example .env

# ���辑 .env 文���，添加你的 API 密钥
# API_KEY=your_openexchangerates_api_key
```

**获���免费 API 密钥**: ���问 [OpenExchangeRates](https://openexchangerates.org/) 注册（���月 1000 ���免费���求���

### 4. 运行���虫

```bash
# 完���流程���爬取价格 → 转换汇率
python nintendo.py
python nintendo_rate_converter.py
```

## ���� 数���输出

### 主要文件

| ���件名 | 描述 |
|--------|------|
| `nintendo_prices.json` | 原���价格数���，包���所有国家的完���信息 |
| `nintendo_prices_cny_sorted.json` | 按人民币价格���序的数据���包含 TOP 10 |

### ���据结构示例

```json
{
  "_top_10_cheapest": [
    {
      "country_code": "AR",
      "country_name": "Argentina",
      "plan": "Family - 12 months",
      "original_price": "ARS 2,500",
      "amount": 2500,
      "currency": "ARS",
      "price_cny": 18.50,
      "url": "https://ec.nintendo.com/AR/es/membership"
    }
  ],
  "by_country": {
    "US": [
      {
        "country_code": "US",
        "country_name": "United States",
        "plan": "Individual - 12 months",
        "original_price": "$19.99",
        "amount": 19.99,
        "currency": "USD",
        "price_cny": 145.20,
        "url": "https://ec.nintendo.com/US/en/membership"
      }
    ]
  }
}
```

## 🌍 ���持的国家/地区

项目支��� 40+ 个国家���地区，包括：

### 亚洲
日本、韩国、香���、新加���、马���西���、���国、印���尼西亚、菲律宾、台湾

### ���美
美国���加拿���、墨西���

### 欧洲
英国、德国、���国、西班牙���意大利、荷兰、瑞士、瑞典、挪威等

### 大洋洲
澳大利���、新西兰

### 南美
巴西���阿根廷、智���、哥伦比亚、秘���

## ����️ ���术栈

| 技��� | 用途 |
|------|------|
| Python 3.9+ | 核心开发语��� |
| Playwright | 浏览器自���化，���理���户端渲��� |
| BeautifulSoup | HTML 解析 |
| OpenExchangeRates API | 实时汇���数��� |

## ���� 项目���构

```
nintendo-switch-online-prices/
├── nintendo.py                      # ���爬虫脚本
���── nintendo_rate_converter.py       # 汇率转���器
├���─ requirements.txt                 # Python 依赖
���── .env.example                     # 环境���量模���
├── .gitignore                       # Git ���略文���
├─��� README.md                        # 项目���档
���─��� nintendo_prices.json            # 原始���格数���（运���后生成���
└── nintendo_prices_cny_sorted.json # ���序后���数据（���行后生成）
```

## 🔧 高���用法

### 单独���行某个模块

```bash
# 仅爬取���格数据
python nintendo.py

# 仅转换汇率（需���先运行 nintendo.py）
python nintendo_rate_converter.py
```

### 查看最便宜的���阅

运��� `nintendo_rate_converter.py` 后，终���会显示 TOP 10 ���便���的订阅���

```
🏆 ���便宜的 TOP 10:
--------------------------------------------------------------------------------
 1. Argentina             | Family - 12 months              | ¥   18.50 (ARS 2500.0)
 2. Turkey                | Family - 12 months              | ¥   32.80 (TRY 450.0)
 3. Brazil                | Individual - 12 months          | ¥   45.20 (BRL 35.0)
...
```

## ���️ 使用说明

- 📚 **用途**: 本项���仅用于���习和研究���的
- ⏱️ **频率**: 内置延迟���制���避免过���请求
- 📊 **准���性**: 价格���据仅供���考，以官方���格为���
- 🌐 **限制**: 某���地区可���有���阅限���

## 🤝 参考���目

本项目参���了以下���秀项目：
- [spotify-prices](https://github.com/SzeMeng76/spotify-prices) - Spotify 价格���虫
- [disneyplus-prices](https://github.com/SzeMeng76/disneyplus-prices) - Disney+ 价格���虫

## 📝 更新���志

- **v1.0** 🎉 初始版本
  - 支持 40+ ���国家/地���
  - Playwright ���览器自动化
  - ���时���率转���
  - TOP 10 排行���

## 📄 许可���

���项目仅���于���习和研究目的���请遵���相关���律和���站服务���款。

---

<div align="center">

**🎮 找到���划算的 Nintendo Switch Online 订阅！**

[开始使���](#-快���开始) • [查看数据](#-���据输出) ��� [技术栈](#️-���术���)

</div>
