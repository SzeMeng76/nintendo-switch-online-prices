#!/usr/bin/env python3
"""
Nintendo Switch Online price converter with CNY conversion and rankings
"""

import json
import requests
import re
import os
from decimal import Decimal, ROUND_HALF_UP, InvalidOperation
from typing import Dict, Any, List

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

API_KEY = os.getenv('API_KEY')
if not API_KEY:
    print("ERROR: API_KEY not found!")
    print("Please set API_KEY in .env file")
    print("Get free API key: https://openexchangerates.org/")
    exit(1)

API_URL = f"https://openexchangerates.org/api/latest.json?app_id={API_KEY}"
INPUT_JSON = 'nintendo_prices.json'
OUTPUT_JSON = 'nintendo_prices_cny_sorted.json'


def get_exchange_rates() -> Dict[str, float]:
    """Get exchange rates"""
    try:
        response = requests.get(API_URL, timeout=10)
        response.raise_for_status()
        data = response.json()

        if 'rates' in data:
            rates = data['rates']
            if 'USD' not in rates:
                rates['USD'] = 1.0
            print("OK - Exchange rates fetched")
            return rates
        else:
            print(f"ERROR - API response: {data.get('description', 'Unknown error')}")
            return None
    except Exception as e:
        print(f"ERROR - Failed to fetch rates: {e}")
        return None


def extract_price_and_currency(price_text: str, default_currency: str) -> tuple:
    """Extract amount and currency from price text"""
    if not price_text:
        return None, default_currency

    cleaned = price_text.strip()

    patterns = [
        r'([A-Z]{3})\s*([\d,\.]+)',
        r'([\d,\.]+)\s*([A-Z]{3})',
        r'([\$€£¥₹₱₩])\s*([\d,\.]+)',
        r'([\d,\.]+)\s*([\$€£¥₹₱₩])',
        r'([\d,\.]+)',
    ]

    for pattern in patterns:
        match = re.search(pattern, cleaned)
        if match:
            groups = match.groups()

            amount_str = None
            currency = default_currency

            if len(groups) == 2:
                for i, g in enumerate(groups):
                    if re.match(r'[\d,\.]+', g):
                        amount_str = g
                        other = groups[1-i]
                        if other and not re.match(r'[\d,\.]+', other):
                            currency = map_currency_symbol(other, default_currency)
                    break
            else:
                amount_str = groups[0]

            if amount_str:
                # 智能处理逗号和点：判断哪个是小数点
                # 规则：
                # - 如果最后的逗号/点距离末尾<=3个字符，那是小数点
                # - 如果>3个字符，那是千位分隔符
                # - 如果同时有逗号和点，后面的是小数点，前面的是千位分隔符

                last_comma = amount_str.rfind(',')
                last_dot = amount_str.rfind('.')

                # 计算距离末尾的字符数
                chars_after_comma = len(amount_str) - last_comma - 1 if last_comma >= 0 else 999
                chars_after_dot = len(amount_str) - last_dot - 1 if last_dot >= 0 else 999

                if last_comma >= 0 and last_dot >= 0:
                    # 同时有逗号和点：后面的是小数点，前面的是千位分隔符
                    if last_comma > last_dot:
                        # 逗号在后：逗号=小数点，点=千位分隔符
                        # 例如：70.899,00
                        amount_str = amount_str.replace('.', '').replace(',', '.')
                    else:
                        # 点在后：点=小数点，逗号=千位分隔符
                        # 例如：1,234.56
                        amount_str = amount_str.replace(',', '')
                elif last_comma >= 0:
                    # 只有逗号：根据距离末尾的字符数判断
                    if chars_after_comma <= 2:
                        # 距离末尾<=2个字符：是小数点（欧洲格式）
                        # 例如：279,90
                        amount_str = amount_str.replace(',', '.')
                    else:
                        # 距离末尾>2个字符：是千位分隔符
                        # 例如：1,399
                        amount_str = amount_str.replace(',', '')
                elif last_dot >= 0:
                    # 只有点：根据距离末尾的字符数判断
                    if chars_after_dot <= 2:
                        # 距离末尾<=2个字符：是小数点
                        # 例如：99.90
                        pass  # 不需要处理
                    else:
                        # 距离末尾>2个字符：是千位分隔符
                        # 例如：10.000
                        amount_str = amount_str.replace('.', '')

                try:
                    amount = Decimal(amount_str)
                    return amount, currency
                except InvalidOperation:
                    continue

    return None, default_currency


def map_currency_symbol(symbol: str, default: str) -> str:
    """Map currency symbol to standard currency code"""
    symbol_map = {
        '$': 'USD', 'USD': 'USD', 'US$': 'USD',
        'EUR': 'EUR', 'GBP': 'GBP', 'JPY': 'JPY', 'CNY': 'CNY',
        'HK$': 'HKD', 'HKD': 'HKD',
        'S$': 'SGD', 'SGD': 'SGD',
        'MYR': 'MYR', 'RM': 'MYR',
        'THB': 'THB',
        'IDR': 'IDR', 'Rp': 'IDR',
        'PHP': 'PHP',
        'KRW': 'KRW',
        'TWD': 'TWD', 'NT$': 'TWD',
        'CAD': 'CAD', 'CA$': 'CAD',
        'MXN': 'MXN', 'MX$': 'MXN',
        'AUD': 'AUD', 'A$': 'AUD',
        'NZD': 'NZD', 'NZ$': 'NZD',
        'BRL': 'BRL', 'R$': 'BRL',
        'ARS': 'ARS',
        'CLP': 'CLP',
        'COP': 'COP',
        'PEN': 'PEN',
        'ZAR': 'ZAR',
        'CHF': 'CHF',
        'SEK': 'SEK',
        'NOK': 'NOK',
        'DKK': 'DKK',
        'PLN': 'PLN',
        'CZK': 'CZK',
        'RUB': 'RUB',
    }

    return symbol_map.get(symbol.upper(), default)


def convert_to_cny(amount: Decimal, currency: str, rates: Dict[str, float]) -> Decimal:
    """Convert amount to CNY"""
    if currency == 'CNY':
        return amount

    if currency not in rates:
        print(f"    WARN - No rate for {currency}")
        return None

    if 'CNY' not in rates:
        print(f"    WARN - No CNY rate")
        return None

    try:
        cny_rate = Decimal(str(rates['CNY']))
        currency_rate = Decimal(str(rates[currency]))

        cny_amount = (amount * cny_rate / currency_rate).quantize(
            Decimal('0.01'), rounding=ROUND_HALF_UP
        )

        return cny_amount
    except Exception as e:
        print(f"    WARN - Conversion failed: {e}")
        return None


def process_prices(input_data: Dict, rates: Dict[str, float]) -> Dict:
    """Process all price data with per-month calculation and category rankings"""
    processed = {}
    all_plans = []

    print("\nProcessing price data...")
    print("=" * 80)

    for country_code, plans in input_data.items():
        print(f"\n[{country_code}] Processing...")

        for plan in plans:
            price_text = plan.get('price', '')
            default_currency = plan.get('currency', 'USD')
            country_name = plan.get('country_name', country_code)
            plan_name = plan.get('plan', 'Unknown Plan')
            plan_type = plan.get('plan_type', 'Unknown')
            duration = plan.get('duration', 'Unknown')
            duration_months = plan.get('duration_months', 1)
            has_expansion_pack = plan.get('has_expansion_pack', False)

            amount, currency = extract_price_and_currency(price_text, default_currency)

            if amount and amount > 0:
                cny_amount = convert_to_cny(amount, currency, rates)

                if cny_amount:
                    cny_per_month = cny_amount / duration_months if duration_months > 0 else cny_amount

                    processed_plan = {
                        'country_code': country_code,
                        'country_name': country_name,
                        'plan': plan_name,
                        'plan_type': plan_type,
                        'duration': duration,
                        'duration_months': duration_months,
                        'has_expansion_pack': has_expansion_pack,
                        'original_price': price_text,
                        'amount': float(amount),
                        'currency': currency,
                        'price_cny_total': float(cny_amount),
                        'price_cny_per_month': float(cny_per_month),
                        'url': plan.get('url', '')
                    }

                    all_plans.append(processed_plan)

                    if duration_months > 1:
                        print(f"    OK - {plan_name}: {currency} {amount} = CNY {cny_amount:.2f} (CNY {cny_per_month:.2f}/mo)")
                    else:
                        print(f"    OK - {plan_name}: {currency} {amount} = CNY {cny_amount:.2f}")
            else:
                print(f"    WARN - Cannot parse: {price_text}")

        if country_code in input_data:
            processed[country_code] = [p for p in all_plans if p['country_code'] == country_code]

    # Filter by plan type, duration, and whether it bundles the Expansion Pack
    individual_12m = [p for p in all_plans if p['plan_type'] == 'Individual' and p['duration_months'] == 12 and not p['has_expansion_pack']]
    family_12m = [p for p in all_plans if p['plan_type'] == 'Family' and p['duration_months'] == 12 and not p['has_expansion_pack']]
    individual_12m_expansion = [p for p in all_plans if p['plan_type'] == 'Individual' and p['duration_months'] == 12 and p['has_expansion_pack']]
    family_12m_expansion = [p for p in all_plans if p['plan_type'] == 'Family' and p['duration_months'] == 12 and p['has_expansion_pack']]

    # Sort by per-month price
    individual_12m_sorted = sorted(individual_12m, key=lambda x: x['price_cny_per_month'])
    family_12m_sorted = sorted(family_12m, key=lambda x: x['price_cny_per_month'])
    individual_12m_expansion_sorted = sorted(individual_12m_expansion, key=lambda x: x['price_cny_per_month'])
    family_12m_expansion_sorted = sorted(family_12m_expansion, key=lambda x: x['price_cny_per_month'])

    result = {
        '_top_10_cheapest_individual_12month': individual_12m_sorted[:10] if len(individual_12m_sorted) >= 10 else individual_12m_sorted,
        '_top_10_cheapest_family_12month': family_12m_sorted[:10] if len(family_12m_sorted) >= 10 else family_12m_sorted,
        '_top_10_cheapest_individual_12month_expansion_pack': individual_12m_expansion_sorted[:10] if len(individual_12m_expansion_sorted) >= 10 else individual_12m_expansion_sorted,
        '_top_10_cheapest_family_12month_expansion_pack': family_12m_expansion_sorted[:10] if len(family_12m_expansion_sorted) >= 10 else family_12m_expansion_sorted,
        'by_country': processed
    }

    return result


def main():
    print("Nintendo Switch Online Price Converter")
    print("=" * 80)

    if not os.path.exists(INPUT_JSON):
        print(f"ERROR - Input file not found: {INPUT_JSON}")
        print("Please run nintendo.py first")
        exit(1)

    print(f"\nReading: {INPUT_JSON}")
    with open(INPUT_JSON, 'r', encoding='utf-8') as f:
        input_data = json.load(f)

    print(f"OK - Loaded {len(input_data)} countries/regions")

    print(f"\nFetching exchange rates...")
    rates = get_exchange_rates()

    if not rates:
        print("ERROR - Cannot fetch rates")
        exit(1)

    processed_data = process_prices(input_data, rates)

    print("\n" + "=" * 80)
    print(f"Saving to: {OUTPUT_JSON}")

    with open(OUTPUT_JSON, 'w', encoding='utf-8') as f:
        json.dump(processed_data, f, ensure_ascii=False, indent=2)

    # Display rankings
    individual_top = processed_data.get('_top_10_cheapest_individual_12month', [])
    family_top = processed_data.get('_top_10_cheapest_family_12month', [])
    individual_expansion_top = processed_data.get('_top_10_cheapest_individual_12month_expansion_pack', [])
    family_expansion_top = processed_data.get('_top_10_cheapest_family_12month_expansion_pack', [])

    print("\n" + "=" * 80)
    print("OK - Conversion completed!")

    if individual_top:
        print(f"\nTOP 10 Cheapest Individual 12-month:")
        print("-" * 80)
        for i, plan in enumerate(individual_top, 1):
            print(f"{i:2d}. {plan['country_name']:20s} | CNY {plan['price_cny_per_month']:6.2f}/mo | Total: CNY {plan['price_cny_total']:7.2f} | {plan['currency']} {plan['amount']}")

    if family_top:
        print(f"\nTOP 10 Cheapest Family 12-month:")
        print("-" * 80)
        for i, plan in enumerate(family_top, 1):
            print(f"{i:2d}. {plan['country_name']:20s} | CNY {plan['price_cny_per_month']:6.2f}/mo | Total: CNY {plan['price_cny_total']:7.2f} | {plan['currency']} {plan['amount']}")

    if individual_expansion_top:
        print(f"\nTOP 10 Cheapest Individual 12-month + Expansion Pack:")
        print("-" * 80)
        for i, plan in enumerate(individual_expansion_top, 1):
            print(f"{i:2d}. {plan['country_name']:20s} | CNY {plan['price_cny_per_month']:6.2f}/mo | Total: CNY {plan['price_cny_total']:7.2f} | {plan['currency']} {plan['amount']}")

    if family_expansion_top:
        print(f"\nTOP 10 Cheapest Family 12-month + Expansion Pack:")
        print("-" * 80)
        for i, plan in enumerate(family_expansion_top, 1):
            print(f"{i:2d}. {plan['country_name']:20s} | CNY {plan['price_cny_per_month']:6.2f}/mo | Total: CNY {plan['price_cny_total']:7.2f} | {plan['currency']} {plan['amount']}")

    print("=" * 80)


if __name__ == '__main__':
    main()
