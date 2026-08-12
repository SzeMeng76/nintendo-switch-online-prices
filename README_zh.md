# 🎮 Nintendo Switch Online 全球价格爬虫

> 自动抓取全球 Nintendo Switch Online 订阅价格，实时汇率转换，找到最便宜的订阅地区

[![Python](https://img.shields.io/badge/Python-3.9+-blue)](https://www.python.org/)
[![Playwright](https://img.shields.io/badge/Playwright-Latest-green)](https://playwright.dev/)

**🌐 语言**: [English](README.md) | 中文

## ✨ 核心功能

| 功能 | 说明 |
|------|------|
| 🌍 **全球价格抓取** | 自动抓取 40+ 个国家/地区的 Nintendo Switch Online 价格 |
| 💱 **实时汇率转换** | 集成 OpenExchangeRates API，将所有价格实时转换为人民币 |
| 🏆 **智能排行榜** | 按均摊月付价格排序，快速找到最便宜的订阅地区 |
| 🤖 **浏览器自动化** | 使用 Playwright 处理客户端渲染页面 |
| 📊 **标准化数据** | 统一的 JSON 格式输出，便于分析和对比 |
| 💳 **均摊月付计算** | 自动计算多月套餐折合每月的价格 |

## 🚀 快速开始

### 前置要求

- Python 3.9+
- 免费的 OpenExchangeRates API 密钥

### 安装步骤

```bash
# 1. 克隆项目
git clone <your-repo-url>
cd nintendo-switch-online-prices

# 2. 安装依赖
pip install -r requirements.txt
playwright install chromium

# 3. 配置 API 密钥
cp .env.example .env
# 编辑 .env 文件，添加你的 API_KEY

# 4. 运行爬虫
python run.py
```

### 🔑 获取 API 密钥

1. 访问 [OpenExchangeRates](https://openexchangerates.org/)
2. 注册免费账户（每月 1000 次免费请求）
3. 获取你的 API 密钥并添加到 `.env` 文件

## 📊 数据输出

### 主要文件

```
nintendo_prices.json              # 原始价格数据
nintendo_prices_cny_sorted.json   # 按人民币排序的数据
```

### 数据结构示例

```json
{
  "_top_10_cheapest_individual_12month": [
    {
      "country_code": "AR",
      "country_name": "Argentina",
      "plan": "Individual - 12 months",
      "plan_type": "Individual",
      "duration": "12 months",
      "duration_months": 12,
      "original_price": "ARS 2,500",
      "amount": 2500,
      "currency": "ARS",
      "price_cny_total": 18.50,
      "price_cny_per_month": 1.54,
      "url": "https://ec.nintendo.com/AR/es/membership"
    }
  ],
  "_top_10_cheapest_family_12month": [ "..." ],
  "by_country": { "US": [ "..." ] }
}
```

## 🌍 支持的国家/地区

项目以 Nintendo 官方公布的 40+ 个市场为目标，覆盖：

**亚太地区**：日本、香港、韩国、新加坡、马来西亚、泰国、台湾、澳大利亚、新西兰、菲律宾

**美洲**：美国、加拿大、墨西哥、巴西、阿根廷、智利、哥伦比亚、秘鲁

**欧洲**：英国、德国、法国、西班牙、意大利、荷兰、奥地利、比利时、保加利亚、克罗地亚、塞浦路斯、捷克、丹麦、爱沙尼亚、芬兰、希腊、匈牙利、爱尔兰、以色列、拉脱维亚、立陶宛、卢森堡、马耳他、挪威、波兰、葡萄牙、罗马尼亚、斯洛伐克、斯洛文尼亚、瑞典、瑞士

**非洲**：南非

## 🛠️ 使用方法

### 方式一：快速运行（推荐）

```bash
python run.py
```

自动运行爬虫和汇率转换，并显示 TOP 10 最便宜的订阅排行榜。

### 方式二：分步运行

```bash
# 步骤 1：运行爬虫
python nintendo.py

# 步骤 2：转换汇率并排序
python nintendo_rate_converter.py
```

### 方式三：测试模式

```bash
# 快速测试几个国家
python test_scraper.py
```

## 📁 项目结构

```
nintendo-switch-online-prices/
├── nintendo.py                      # 主爬虫脚本
├── nintendo_rate_converter.py       # 汇率转换与排行榜
├── run.py                           # 快速运行脚本
├── test_scraper.py                  # 测试脚本
├── requirements.txt                 # Python 依赖
├── .env.example                     # 环境变量模板
├── .gitignore                       # Git 忽略文件
├── README.md                        # 英文文档
├── README_zh.md                     # 中文文档
├── .github/workflows/
│   └── weekly-scraper.yml          # GitHub Actions 自动化
├── nintendo_prices.json            # 原始数据（运行后生成）
└── nintendo_prices_cny_sorted.json # 排序数据（运行后生成）
```

## 🤖 GitHub Actions 自动化

项目包含 GitHub Actions 工作流，可以每周自动运行爬虫并提交更新后的数据。

### 设置步骤

1. Fork 这个项目到你的 GitHub
2. 进入 **Settings** → **Secrets and variables** → **Actions**
3. 添加 Secret：`API_KEY` = 你的 OpenExchangeRates API 密钥
4. 工作流会在每周日自动运行

## 🔧 技术栈

| 技术 | 用途 | 版本 |
|------|------|------|
| Python | 核心开发语言 | 3.9+ |
| Playwright | 浏览器自动化，处理客户端渲染 | Latest |
| BeautifulSoup | HTML 解析 | 4.11.0+ |
| OpenExchangeRates API | 实时汇率数据 | v6 |

## 💡 使用建议

### 订阅便宜地区的注意事项

1. **账号地区设置**：需要将 Nintendo 账号地区改为目标国家
2. **支付方式**：某些地区可能需要当地支付方式
3. **IP 地址**：可能需要对应地区的 IP 才能购买
4. **服务限制**：不同地区的服务内容可能有差异

### 价格对比技巧

- 关注 **Family Plan 12 个月** 套餐，通常最划算
- 考虑与朋友分摊 Family Plan 费用
- 定期查看价格变化，汇率波动可能影响实际价格

## ⚠️ 免责声明

- 本项目仅用于学习和研究目的
- 价格数据仅供参考，实际价格以官方为准
- 请遵守 Nintendo 的服务条款
- 跨区购买可能存在风险，请谨慎决定

## 🤝 参考项目

本项目参考了以下项目的结构：

- [spotify-prices](https://github.com/SzeMeng76/spotify-prices) - Spotify 全球价格爬虫
- [disneyplus-prices](https://github.com/SzeMeng76/disneyplus-prices) - Disney+ 全球价格爬虫

## 📝 更新日志

### v1.0.0

- 🎉 初始版本发布
- ✅ 支持 40+ 个国家/地区
- ✅ Playwright 浏览器自动化
- ✅ 实时汇率转换
- ✅ Individual / Family 12 个月套餐 TOP 10 排行榜
- ✅ GitHub Actions 自动化

## 📄 许可证

本项目仅用于学习和研究目的。请遵守相关法律和网站服务条款。

---

<div align="center">

**🎮 找到最划算的 Nintendo Switch Online 订阅！**

[开始使用](#-快速开始) • [查看数据](#-数据输出) • [技术栈](#-技术栈)

</div>
