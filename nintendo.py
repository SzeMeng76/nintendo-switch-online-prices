#!/usr/bin/env python3
"""
Nintendo Switch Online 价格爬虫
使用 Playwright 自动化浏览器获取各国 Nintendo Switch Online 订阅价格
精确识别套餐类型和时长，便于后续生成分类排行榜
"""

import re
import asyncio
import json
from typing import Any, Dict, List
from bs4 import BeautifulSoup
from playwright.async_api import async_playwright, Page


# Nintendo Switch Online 支持的国家/地区列表
# 基于 Nintendo eShop 官方可用地区整理（共 49 个市场）：
# 亚太 9 个、美洲 8 个、欧洲 30 个、中东与非洲 2 个
NINTENDO_COUNTRIES = {
    # 亚太地区
    "JP": {"name": "Japan", "lang": "ja", "currency": "JPY"},
    "HK": {"name": "Hong Kong", "lang": "en", "currency": "HKD"},
    "KR": {"name": "South Korea", "lang": "ko", "currency": "KRW"},
    "SG": {"name": "Singapore", "lang": "en", "currency": "SGD"},
    "MY": {"name": "Malaysia", "lang": "en", "currency": "MYR"},
    "TH": {"name": "Thailand", "lang": "en", "currency": "THB"},
    "TW": {"name": "Taiwan", "lang": "zh-Hant", "currency": "TWD"},
    "AU": {"name": "Australia", "lang": "en", "currency": "AUD"},
    "NZ": {"name": "New Zealand", "lang": "en", "currency": "NZD"},

    # 美洲
    "US": {"name": "United States", "lang": "en", "currency": "USD"},
    "CA": {"name": "Canada", "lang": "en", "currency": "CAD"},
    "MX": {"name": "Mexico", "lang": "es", "currency": "MXN"},
    "BR": {"name": "Brazil", "lang": "pt", "currency": "BRL"},
    "AR": {"name": "Argentina", "lang": "es", "currency": "ARS"},
    "CL": {"name": "Chile", "lang": "es", "currency": "CLP"},
    "CO": {"name": "Colombia", "lang": "es", "currency": "COP"},
    "PE": {"name": "Peru", "lang": "es", "currency": "PEN"},

    # 欧洲
    "GB": {"name": "United Kingdom", "lang": "en", "currency": "GBP"},
    "DE": {"name": "Germany", "lang": "de", "currency": "EUR"},
    "FR": {"name": "France", "lang": "fr", "currency": "EUR"},
    "ES": {"name": "Spain", "lang": "es", "currency": "EUR"},
    "IT": {"name": "Italy", "lang": "it", "currency": "EUR"},
    "NL": {"name": "Netherlands", "lang": "nl", "currency": "EUR"},
    "AT": {"name": "Austria", "lang": "de", "currency": "EUR"},
    "BE": {"name": "Belgium", "lang": "en", "currency": "EUR"},
    "BG": {"name": "Bulgaria", "lang": "en", "currency": "BGN"},
    "HR": {"name": "Croatia", "lang": "en", "currency": "EUR"},
    "CY": {"name": "Cyprus", "lang": "en", "currency": "EUR"},
    "CZ": {"name": "Czech Republic", "lang": "cs", "currency": "CZK"},
    "DK": {"name": "Denmark", "lang": "da", "currency": "DKK"},
    "EE": {"name": "Estonia", "lang": "en", "currency": "EUR"},
    "FI": {"name": "Finland", "lang": "fi", "currency": "EUR"},
    "GR": {"name": "Greece", "lang": "en", "currency": "EUR"},
    "HU": {"name": "Hungary", "lang": "en", "currency": "HUF"},
    "IE": {"name": "Ireland", "lang": "en", "currency": "EUR"},
    "LV": {"name": "Latvia", "lang": "en", "currency": "EUR"},
    "LT": {"name": "Lithuania", "lang": "en", "currency": "EUR"},
    "LU": {"name": "Luxembourg", "lang": "en", "currency": "EUR"},
    "MT": {"name": "Malta", "lang": "en", "currency": "EUR"},
    "NO": {"name": "Norway", "lang": "no", "currency": "NOK"},
    "PL": {"name": "Poland", "lang": "pl", "currency": "PLN"},
    "PT": {"name": "Portugal", "lang": "pt", "currency": "EUR"},
    "RO": {"name": "Romania", "lang": "en", "currency": "RON"},
    "SK": {"name": "Slovakia", "lang": "en", "currency": "EUR"},
    "SI": {"name": "Slovenia", "lang": "en", "currency": "EUR"},
    "SE": {"name": "Sweden", "lang": "sv", "currency": "SEK"},
    "CH": {"name": "Switzerland", "lang": "de", "currency": "CHF"},

    # 中东与非洲
    "IL": {"name": "Israel", "lang": "en", "currency": "ILS"},
    "ZA": {"name": "South Africa", "lang": "en", "currency": "ZAR"},
}

# 价格符号字符集，用于正则匹配（美元/欧元/英镑/日元/卢比/比索/谢克尔/卢比(巴)/奈拉/塞地/科朗/韩元）
CURRENCY_SYMBOLS = "\\$\u20ac\u00a3\u00a5\u20b9\u20b1\u20aa\u20a8\u20a6\u20b5\u20a1\u20a9"


def extract_prices_from_html(html: str, country_code: str) -> List[Dict[str, Any]]:
    """从页面 HTML 中提取价格信息，精确识别套餐类型和时长"""
    soup = BeautifulSoup(html, 'html.parser')
    plans = []

    price_symbol_pattern = (
        r'([' + CURRENCY_SYMBOLS + r']|[A-Z]{2,3})\s*([\d,\.]+)'
        r'|([\d,\.]+)\s*([' + CURRENCY_SYMBOLS + r']|[A-Z]{2,3})'
    )

    try:
        # 查找所有可能包含价格的文本节点
        all_elements = soup.find_all(['div', 'span', 'p', 'td', 'th', 'li', 'button', 'a'])

        for elem in all_elements:
            elem_text = elem.get_text(' ', strip=True)

            # 跳过过长或过短的文本
            if len(elem_text) > 500 or len(elem_text) < 3:
                continue

            # 检查是否包含价格
            price_match = re.search(price_symbol_pattern, elem_text)
            if not price_match:
                continue

            # 提取实际价格字符串（包含货币符号和数字）
            price_text = price_match.group(0)

            # 获取更多上下文 - 查找父元素文本，帮助判断套餐类型和时长
            context_text = elem_text
            if elem.parent:
                context_text += " " + elem.parent.get_text(' ', strip=True)[:300]

            # 识别套餐类型
            plan_type = "Unknown"
            if re.search(r'\bfamily\b|家庭|familia|famille|familie', context_text, re.IGNORECASE):
                plan_type = "Family"
            elif re.search(r'\bindividual\b|個人|个人|personal|solo', context_text, re.IGNORECASE):
                plan_type = "Individual"

            # 识别时长（更精确）
            duration = None
            duration_months = None

            # 12 个月 / 1 年
            if re.search(r'12\s*month|12\s*meses|12\s*mois|12\s*\u30f6\u6708|12\s*\u4e2a\u6708|1\s*year|1\s*a\u00f1o|1\s*jahr|\u5e74\u9593', context_text, re.IGNORECASE):
                duration = "12 months"
                duration_months = 12
            # 3 个月
            elif re.search(r'3\s*month|3\s*meses|3\s*mois|3\s*ヶ月|3\s*个月', context_text, re.IGNORECASE):
                duration = "3 months"
                duration_months = 3
            # 1 个月
            elif re.search(r'1\s*month|1\s*meses|1\s*mois|1\s*ヶ月|1\s*个月|monthly|mensual', context_text, re.IGNORECASE):
                duration = "1 month"
                duration_months = 1

            # 只保留同时识别出套餐类型和时长的数据
            if plan_type != "Unknown" and duration:
                plans.append({
                    'plan': f"{plan_type} - {duration}",
                    'plan_type': plan_type,
                    'duration': duration,
                    'duration_months': duration_months,
                    'price': price_text,
                    'raw_context': context_text[:200]  # 保留上下文，便于调试
                })

    except Exception as e:
        print(f"    WARNING - Parse error ({country_code}): {e}")

    return plans


async def fetch_country_prices(page: Page, country_code: str, country_info: Dict[str, str]) -> List[Dict[str, Any]]:
    """获取指定国家的价格信息"""
    lang = country_info['lang']
    url = f"https://ec.nintendo.com/{country_code}/{lang}/membership"

    try:
        # 访问页面
        await page.goto(url, wait_until='domcontentloaded', timeout=30000)

        # 等待页面渲染完成 - Nintendo 的价格通常需要等待 JavaScript 渲染
        await page.wait_for_timeout(3000)

        # 等待可能包含价格的元素出现
        try:
            await page.wait_for_selector('div, span, p', timeout=5000)
        except Exception:
            pass

        # 获取页面 HTML
        html = await page.content()

        # 提取价格信息
        plans = extract_prices_from_html(html, country_code)

        # 为每个套餐附加国家信息
        for plan in plans:
            plan['country_code'] = country_code
            plan['country_name'] = country_info['name']
            plan['currency'] = country_info['currency']
            plan['url'] = url

        # 去重：相同的 (plan_type, duration_months, price) 只保留一个
        seen = set()
        unique_plans = []
        for plan in plans:
            key = (plan['plan_type'], plan['duration_months'], plan['price'])
            if key not in seen:
                seen.add(key)
                unique_plans.append(plan)

        return unique_plans

    except Exception as e:
        print(f"    FAIL - Fetch failed ({country_code}): {e}")
        return []


async def main():
    """主函数"""
    results: Dict[str, Any] = {}

    async with async_playwright() as p:
        # 启动浏览器
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(
            viewport={'width': 1920, 'height': 1080},
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        )
        page = await context.new_page()

        print(f"Starting to scrape {len(NINTENDO_COUNTRIES)} countries/regions...")
        print("=" * 80)

        for country_code, country_info in NINTENDO_COUNTRIES.items():
            print(f"[{country_code}] {country_info['name']} ({country_info['currency']})...")

            plans = await fetch_country_prices(page, country_code, country_info)

            if plans:
                results[country_code] = plans
                print(f"    OK - Found {len(plans)} plans")
            else:
                print("    WARN - No price data found")

            # 添加延迟，避免请求过快
            await asyncio.sleep(1)

        await browser.close()

    return results


if __name__ == '__main__':
    print("Nintendo Switch Online Price Scraper")
    print("=" * 80)

    # 运行爬虫
    all_prices = asyncio.run(main())

    if not all_prices:
        raise SystemExit("FAIL - No data scraped, aborting")

    # 保存结果
    output_file = 'nintendo_prices.json'

    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(all_prices, f, ensure_ascii=False, indent=2)

    print("=" * 80)
    print("OK - Scraping completed!")
    print(f"Saved to: {output_file}")
    print(f"Successfully scraped {len(all_prices)} countries/regions")
