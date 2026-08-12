# 🎮 Nintendo Switch Online Global Price Tracker

> Automatically scrape global Nintendo Switch Online subscription prices with real-time currency conversion to find the most affordable regions

[![Python](https://img.shields.io/badge/Python-3.9+-blue)](https://www.python.org/)
[![Playwright](https://img.shields.io/badge/Playwright-Latest-green)](https://playwright.dev/)

**🌐 Language**: English | [中文](README_zh.md)

## ✨ Core Features

| Feature | Description |
|---------|-------------|
| 🌍 **Global Price Scraping** | Automatically scrape Nintendo Switch Online prices from 40+ countries/regions |
| 💱 **Real-time Currency Conversion** | Integrated OpenExchangeRates API, convert all prices to CNY in real-time |
| 🏆 **Smart Ranking System** | Rank by per-month price, instantly find the cheapest subscription regions |
| 🤖 **Browser Automation** | Uses Playwright to handle client-side rendered pages |
| 📊 **Standardized Data** | Unified JSON output format for easy analysis and comparison |
| 💳 **Per-month Price Calculation** | Automatically calculates the equivalent monthly price for multi-month plans |

## 🚀 Quick Start

### Prerequisites
- Python 3.9+
- Free [OpenExchangeRates API Key](https://openexchangerates.org/)

### Installation

```bash
# 1. Clone the repository
git clone <your-repo-url>
cd nintendo-switch-online-prices

# 2. Install dependencies
pip install -r requirements.txt
playwright install chromium

# 3. Configure API key
cp .env.example .env
# Edit .env file and add your API_KEY

# 4. Run the scraper
python run.py
```

### 🔑 API Key Configuration

1. Visit [OpenExchangeRates](https://openexchangerates.org/) to register
2. Get a free API key (1000 free requests per month)
3. Add it to your `.env` file

## 📊 Data Output

### Main Files

```
nintendo_prices.json              # Raw price data
nintendo_prices_cny_sorted.json   # CNY-converted and ranked data
```

### Data Structure Example

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

## 🌍 Supported Countries/Regions

The project targets Nintendo's official 40+ market list, covering:

**Asia Pacific**: Japan, Hong Kong, South Korea, Singapore, Malaysia, Thailand, Taiwan, Australia, New Zealand, Philippines

**Americas**: United States, Canada, Mexico, Brazil, Argentina, Chile, Colombia, Peru

**Europe**: United Kingdom, Germany, France, Spain, Italy, Netherlands, Austria, Belgium, Bulgaria, Croatia, Cyprus, Czech Republic, Denmark, Estonia, Finland, Greece, Hungary, Ireland, Israel, Latvia, Lithuania, Luxembourg, Malta, Norway, Poland, Portugal, Romania, Slovakia, Slovenia, Sweden, Switzerland

**Africa**: South Africa

## 🛠️ Usage

### Quick Run (Recommended)

```bash
python run.py
```

This runs the full pipeline (scraping + conversion) and prints the TOP 10 cheapest rankings.

### Step by Step

```bash
# Step 1: Scrape prices
python nintendo.py

# Step 2: Convert currency and rank
python nintendo_rate_converter.py
```

### Test Mode

```bash
# Quickly test a few countries
python test_scraper.py
```

## 📁 Project Structure

```
nintendo-switch-online-prices/
├── nintendo.py                      # Main scraper script
├── nintendo_rate_converter.py       # Currency conversion & ranking
├── run.py                           # Quick-run helper
├── test_scraper.py                  # Test script
├── requirements.txt                 # Python dependencies
├── .env.example                     # Environment variable template
├── .gitignore                       # Git ignore rules
├── README.md                        # English documentation
├── README_zh.md                     # Chinese documentation
├── .github/workflows/
│   └── weekly-scraper.yml          # GitHub Actions automation
├── nintendo_prices.json            # Raw data (generated after running)
└── nintendo_prices_cny_sorted.json # Ranked data (generated after running)
```

## 🤖 GitHub Actions Automation

The project includes a GitHub Actions workflow that runs the scraper weekly and commits updated data.

### Setup

1. Fork this project to your GitHub account
2. Go to **Settings** → **Secrets and variables** → **Actions**
3. Add a secret: `API_KEY` = your OpenExchangeRates API key
4. The workflow runs automatically every Sunday

## 🔧 Tech Stack

| Technology | Purpose | Version |
|------------|---------|---------|
| Python | Core development language | 3.9+ |
| Playwright | Browser automation for client-side rendering | Latest |
| BeautifulSoup | HTML parsing | 4.11.0+ |
| OpenExchangeRates API | Real-time exchange rate data | v6 |

## ⚠️ Usage Guidelines

- 📚 **Purpose**: For educational and research purposes only, please comply with website terms of service
- ⏱️ **Frequency**: Built-in delay mechanisms to avoid excessive requests
- 📊 **Accuracy**: Price data is for reference only, official prices prevail
- 🌐 **Limitations**: Some regions may have subscription restrictions

## 🤝 Reference Projects

This project references the structure of the following projects:
- [spotify-prices](https://github.com/SzeMeng76/spotify-prices) - Spotify global price scraper
- [disneyplus-prices](https://github.com/SzeMeng76/disneyplus-prices) - Disney+ global price scraper

## 📝 Changelog

- **v1.0** 🎉 Initial release
  - Support for 40+ countries/regions
  - Playwright browser automation
  - Real-time currency conversion
  - TOP 10 rankings for Individual and Family 12-month plans
  - GitHub Actions automation

## 📄 License

This project is for educational and research purposes only. Please comply with relevant laws and website terms of service.

---

<div align="center">

**🎮 Find the best Nintendo Switch Online subscription deals worldwide!**

[Get Started](#-quick-start) • [View Data](#-data-output) • [Tech Stack](#-tech-stack)

</div>
