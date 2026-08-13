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
    "HK": {"name": "Hong Kong", "lang": "zh", "currency": "HKD"},
    "KR": {"name": "South Korea", "lang": "ko", "currency": "KRW"},
    "SG": {"name": "Singapore", "lang": "en", "currency": "SGD"},
    "MY": {"name": "Malaysia", "lang": "en", "currency": "MYR"},
    "TH": {"name": "Thailand", "lang": "en", "currency": "THB"},
    "TW": {"name": "Taiwan", "lang": "zh", "currency": "TWD"},
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
    "BG": {"name": "Bulgaria", "lang": "en", "currency": "EUR"},  # Nintendo uses EUR despite local BGN
    "HR": {"name": "Croatia", "lang": "en", "currency": "EUR"},
    "CY": {"name": "Cyprus", "lang": "en", "currency": "EUR"},
    "CZ": {"name": "Czech Republic", "lang": "cs", "currency": "CZK"},
    "DK": {"name": "Denmark", "lang": "da", "currency": "DKK"},
    "EE": {"name": "Estonia", "lang": "en", "currency": "EUR"},
    "FI": {"name": "Finland", "lang": "fi", "currency": "EUR"},
    "GR": {"name": "Greece", "lang": "en", "currency": "EUR"},
    "HU": {"name": "Hungary", "lang": "en", "currency": "EUR"},  # Nintendo uses EUR despite local HUF
    "IE": {"name": "Ireland", "lang": "en", "currency": "EUR"},
    "LV": {"name": "Latvia", "lang": "en", "currency": "EUR"},
    "LT": {"name": "Lithuania", "lang": "en", "currency": "EUR"},
    "LU": {"name": "Luxembourg", "lang": "en", "currency": "EUR"},
    "MT": {"name": "Malta", "lang": "en", "currency": "EUR"},
    "NO": {"name": "Norway", "lang": "no", "currency": "NOK"},
    "PL": {"name": "Poland", "lang": "pl", "currency": "PLN"},
    "PT": {"name": "Portugal", "lang": "pt", "currency": "EUR"},
    "RO": {"name": "Romania", "lang": "en", "currency": "EUR"},  # Nintendo uses EUR despite local RON
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

# Expansion Pack（追加内容包）关键词，覆盖各官网语言版本
# 英/法/德/西/意/葡/日/中(简繁)/韩
EXPANSION_PACK_PATTERN = re.compile(
    r'expansion\s*pack|pack\s*additionnel|pass\s*additionnel|erweiterungspaket|erweiterung|'
    r'paquete\s*de\s*expansi[oó]n|pacchetto\s*aggiuntivo|pacote\s*adicional|'
    r'追加パック|追加内容包|追加內容包|扩充包|擴充包|추가팩',
    re.IGNORECASE
)


def extract_prices_from_html(html: str, country_code: str) -> List[Dict[str, Any]]:
    """从页面 HTML 中提取价格信息，精确识别套餐类型和时长"""
    soup = BeautifulSoup(html, 'html.parser')
    plans = []

    # 匹配货币符号和代码（显式列出所有支持的货币代码，避免误匹配任意3个大写字母）
    # 日文特殊处理：支持"400円"格式
    currency_codes = r'USD|EUR|GBP|JPY|CNY|HKD|SGD|MYR|THB|IDR|PHP|KRW|TWD|CAD|MXN|AUD|NZD|BRL|ARS|CLP|COP|PEN|ZAR|CHF|SEK|NOK|DKK|PLN|CZK|RUB|ILS'
    price_symbol_pattern = (
        r'(S\$|HK\$|NT\$|CA\$|NZ\$|AU\$|US\$|MX\$|A\$|R\$|RM\s*|Rp\s*|[' + CURRENCY_SYMBOLS + r']|' + currency_codes + r')\s*([\d,\.]+)'
        r'|([\d,\.]+)\s*(S\$|HK\$|NT\$|CA\$|NZ\$|AU\$|US\$|MX\$|A\$|R\$|RM|Rp|円|[' + CURRENCY_SYMBOLS + r']|' + currency_codes + r')'
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

            # 跳过"每月均价"说明文字（Equivalent to X per month, Pari a X al mese等）
            if re.search(r'equivalent|per\s*month|per\s*30|/\s*month|/\s*30|pari\s+a|al\s+mese|月均|每月|一個月約|一个月约', elem_text, re.IGNORECASE):
                continue


            # 构建上下文：向上爬10层寻找套餐信息容器
            context_parts = [elem_text]
            current = elem.parent
            for _ in range(10):
                if current and current.name:
                    parent_text = current.get_text(' ', strip=True)
                    # 限制单个父元素不超过500字符（避免包含整页）
                    if len(parent_text) < 500:
                        context_parts.append(parent_text)
                        current = current.parent
                    else:
                        break
                else:
                    break

            context_text = " ".join(context_parts)[:800]

            # 识别套餐类型：优先在当前元素查找，避免跨套餐混淆
            plan_type = "Unknown"
            if re.search(r'\bfamily\b|家庭|ファミリー|familia|famille|familie', elem_text, re.IGNORECASE):
                plan_type = "Family"
            elif re.search(r'\bindividual\b|個人|个人|personal|solo', elem_text, re.IGNORECASE):
                plan_type = "Individual"
            elif re.search(r'\bfamily\b|家庭|ファミリー|familia|famille|familie', context_text, re.IGNORECASE):
                plan_type = "Family"
            elif re.search(r'\bindividual\b|個人|个人|personal|solo', context_text, re.IGNORECASE):
                plan_type = "Individual"

            # 仍未识别出套餐类型时（价格与套餐标题之间夹着长段免费试用/法律说明文字，
            # 被上面500字符上限截断导致爬不到），单独再向上爬，只用于判断类型、不限制长度
            if plan_type == "Unknown":
                type_ancestor = elem.parent
                for _ in range(25):
                    if not type_ancestor or not type_ancestor.name:
                        break
                    ancestor_text = type_ancestor.get_text(' ', strip=True)
                    if re.search(r'\bfamily\b|家庭|ファミリー|familia|famille|familie', ancestor_text, re.IGNORECASE):
                        plan_type = "Family"
                        break
                    elif re.search(r'\bindividual\b|個人|个人|personal|solo', ancestor_text, re.IGNORECASE):
                        plan_type = "Individual"
                        break
                    type_ancestor = type_ancestor.parent

            # 识别时长：优先在当前元素查找
            duration = None
            duration_months = None

            # 先在当前元素内查找（繁简体中文都支持，日文支持ヶ月和か月两种写法）
            if re.search(r'12\s*month|12\s*meses|12\s*mois|12\s*ヶ月|12\s*か月|12\s*个月|12\s*個月|1\s*year|1\s*año|1\s*jahr|年間', elem_text, re.IGNORECASE):
                duration = "12 months"
                duration_months = 12
            elif re.search(r'3\s*month|3\s*meses|3\s*mois|3\s*ヶ月|3\s*か月|3\s*个月|3\s*個月', elem_text, re.IGNORECASE):
                duration = "3 months"
                duration_months = 3
            elif re.search(r'1\s*month|1\s*meses|1\s*mois|1\s*ヶ月|1\s*か月|1\s*个月|1\s*個月|monthly|mensual', elem_text, re.IGNORECASE):
                duration = "1 month"
                duration_months = 1

            # 当前元素没找到时长才查上下文，但只在价格**前面**的文本内搜索（避免误匹配后续套餐）
            if duration is None:
                # 找价格在context_text中的位置
                price_pos = context_text.find(price_text)
                if price_pos >= 0:
                    # 只在价格**前面**100字符范围内搜索时长（不包括后面的文本）
                    start = max(0, price_pos - 100)
                    local_context = context_text[start:price_pos + len(price_text)]
                else:
                    local_context = context_text[:len(context_text)//2]  # 前半部分

                # 在局部上下文里搜索，按12/3/1顺序（繁简体中文都支持，日文支持ヶ月和か月两种写法）
                if re.search(r'12\s*month|12\s*meses|12\s*mois|12\s*ヶ月|12\s*か月|12\s*个月|12\s*個月|1\s*year|1\s*año|1\s*jahr|年間', local_context, re.IGNORECASE):
                    duration = "12 months"
                    duration_months = 12
                elif re.search(r'3\s*month|3\s*meses|3\s*mois|3\s*ヶ月|3\s*か月|3\s*个月|3\s*個月', local_context, re.IGNORECASE):
                    duration = "3 months"
                    duration_months = 3
                elif re.search(r'1\s*month|1\s*meses|1\s*mois|1\s*ヶ月|1\s*か月|1\s*个月|1\s*個月|monthly|mensual', local_context, re.IGNORECASE):
                    duration = "1 month"
                    duration_months = 1

            # 识别是否为 Expansion Pack 套餐（当前元素或上下文中出现关键词即可）
            has_expansion_pack = bool(EXPANSION_PACK_PATTERN.search(elem_text) or EXPANSION_PACK_PATTERN.search(context_text))

            # 只保留同时识别出套餐类型和时长的数据
            if plan_type != "Unknown" and duration:
                plan_name = f"{plan_type} - {duration}"
                if has_expansion_pack:
                    plan_name += " + Expansion Pack"

                plans.append({
                    'plan': plan_name,
                    'plan_type': plan_type,
                    'duration': duration,
                    'duration_months': duration_months,
                    'has_expansion_pack': has_expansion_pack,
                    'price': price_text,
                    'raw_context': context_text[:200]
                })

    except Exception as e:
        print(f"    WARNING - Parse error ({country_code}): {e}")

    # 去重：同一个(价格, 套餐类型, 时长, 是否含Expansion Pack)组合只保留一个
    seen = set()
    unique_plans = []
    for plan in plans:
        key = (plan['price'], plan['plan_type'], plan['duration'], plan['has_expansion_pack'])
        if key not in seen:
            seen.add(key)
            unique_plans.append(plan)

    return unique_plans


def extract_prices_from_text(text: str, country_code: str) -> List[Dict[str, Any]]:
    """从渲染后的纯文本中提取价格信息（备用方法，用于动态页面）"""
    plans = []

    # 货币符号和代码
    currency_codes = r'USD|EUR|GBP|JPY|CNY|HKD|SGD|MYR|THB|IDR|PHP|KRW|TWD|CAD|MXN|AUD|NZD|BRL|ARS|CLP|COP|PEN|ZAR|CHF|SEK|NOK|DKK|PLN|CZK|RUB|ILS'
    price_pattern = (
        r'(S\$|HK\$|NT\$|CA\$|NZ\$|AU\$|US\$|MX\$|A\$|R\$|RM\s*|Rp\s*|[' + CURRENCY_SYMBOLS + r']|' + currency_codes + r')\s*([\d,\.]+)'
        r'|([\d,\.]+)\s*(S\$|HK\$|NT\$|CA\$|NZ\$|AU\$|US\$|MX\$|A\$|R\$|RM|Rp|円|[' + CURRENCY_SYMBOLS + r']|' + currency_codes + r')'
    )

    # 按行分割文本
    lines = text.split('\n')

    # 查找价格所在行的上下文（前后各3行）
    for i, line in enumerate(lines):
        price_match = re.search(price_pattern, line.strip())
        if not price_match:
            continue

        # 跳过"相当于每月"、"折扣"等派生价格和说明文本
        if re.search(r'entspricht|equivalent|equivale|équivaut|pari\s+a|al\s+mese|相当于|rabatt|discount|descuento|remise|割引|tag/|day/|día/', line, re.IGNORECASE):
            continue

        # 提取价格文本
        price_text = line.strip()

        # 获取上下文（前5行到后2行，重点向上查找套餐标题）
        context_start = max(0, i - 5)
        context_end = min(len(lines), i + 3)
        context_lines = lines[context_start:context_end]
        context_text = ' '.join(l.strip() for l in context_lines if l.strip())

        # 识别套餐类型
        plan_type = 'Individual'
        family_pattern = re.compile(r'family|famil|familia|famille|familie|家庭|ファミリー', re.IGNORECASE)
        if family_pattern.search(context_text):
            plan_type = 'Family'

        # 识别时长
        duration = 'Unknown'
        duration_months = 1

        # 12个月
        if re.search(r'12\s*month|12\s*mes|12\s*mois|12\s*monate|12\s*månader|12\s*mies|12\s*mån|12.*month|12.*mes|365\s*day|12.*個月|12.*个月|12.*ヶ月', context_text, re.IGNORECASE):
            duration = '12 months'
            duration_months = 12
        # 3个月
        elif re.search(r'3\s*month|3\s*mes|3\s*mois|3\s*monate|3\s*månader|3\s*mies|3\s*mån|90\s*day|3.*month|3.*mes|3.*個月|3.*个月|3.*ヶ月', context_text, re.IGNORECASE):
            duration = '3 months'
            duration_months = 3
        # 1个月
        elif re.search(r'1\s*month|1\s*mes|1\s*mois|1\s*monat|1\s*månad|30\s*day|1.*month|1.*mes|1.*個月|1.*个月|1.*ヶ月', context_text, re.IGNORECASE):
            duration = '1 month'
            duration_months = 1

        # 构建套餐名称
        plan_name = f"{plan_type} - {duration}"
        has_expansion_pack = bool(EXPANSION_PACK_PATTERN.search(context_text))
        if has_expansion_pack:
            plan_name += ' + Expansion Pack'

        plans.append({
            'plan': plan_name,
            'plan_type': plan_type,
            'duration': duration,
            'duration_months': duration_months,
            'has_expansion_pack': has_expansion_pack,
            'price': price_text,
            'raw_context': context_text[:300]
        })

    # 去重
    seen = set()
    unique_plans = []
    for plan in plans:
        key = (plan['price'], plan['plan_type'], plan['duration'], plan['has_expansion_pack'])
        if key not in seen:
            seen.add(key)
            unique_plans.append(plan)

    return unique_plans


async def fetch_country_prices(page: Page, country_code: str, country_info: Dict[str, str]) -> List[Dict[str, Any]]:
    """获取指定国家的价格信息"""
    lang = country_info['lang']
    url = f"https://ec.nintendo.com/{country_code}/{lang}/membership"

    try:
        # 访问页面并等待网络空闲
        await page.goto(url, wait_until='networkidle', timeout=60000)

        # 额外等待确保 JavaScript 完全执行
        await page.wait_for_timeout(3000)

        # 获取页面 HTML
        html = await page.content()

        # 提取价格信息
        plans = extract_prices_from_html(html, country_code)

        # 如果HTML提取失败，尝试从渲染后的文本提取（某些页面价格是动态插入的）
        if not plans:
            body_text = await page.locator('body').inner_text()
            plans = extract_prices_from_text(body_text, country_code)

        # 为每个套餐附加国家信息
        for plan in plans:
            plan['country_code'] = country_code
            plan['country_name'] = country_info['name']
            plan['currency'] = country_info['currency']
            plan['url'] = url

        # 去重：相同的 (plan_type, duration_months, price, has_expansion_pack) 只保留一个
        seen = set()
        unique_plans = []
        for plan in plans:
            key = (plan['plan_type'], plan['duration_months'], plan['price'], plan.get('has_expansion_pack', False))
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
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        )
        page = await context.new_page()

        print(f"Nintendo Switch Online Price Scraper")
        print(f"Total countries/regions: {len(NINTENDO_COUNTRIES)}")
        print("=" * 80)

        # 遍历所有国家
        for country_code, country_info in NINTENDO_COUNTRIES.items():
            print(f"\n[{country_code}] {country_info['name']}...")

            plans = await fetch_country_prices(page, country_code, country_info)

            if plans:
                print(f"    OK - Found {len(plans)} plans")
                results[country_code] = plans
            else:
                print(f"    WARN - No plans found")
                results[country_code] = []

            # 礼貌延迟，避免请求过快
            await asyncio.sleep(1)

        await browser.close()

    return results


if __name__ == '__main__':
    print("Starting scraper...")
    results = asyncio.run(main())

    # 保存结果
    output_file = 'nintendo_prices.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

    print("\n" + "=" * 80)
    print(f"OK - Saved to {output_file}")
    print(f"Total countries scraped: {len(results)}")
    print("=" * 80)
