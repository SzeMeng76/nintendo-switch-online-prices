#!/usr/bin/env python3
"""
Nintendo Switch Online 价格爬虫测试脚本
快速测试几个国家的价格抓取是否正常
"""

import asyncio
from nintendo import fetch_country_prices, NINTENDO_COUNTRIES
from playwright.async_api import async_playwright


async def test_scraper():
    """测试爬虫功能"""
    print("Nintendo Switch Online 爬虫测试")
    print("=" * 80)

    # 选择几个代表性国家进行测试
    test_countries = {
        "US": NINTENDO_COUNTRIES["US"],
        "JP": NINTENDO_COUNTRIES["JP"],
        "MY": NINTENDO_COUNTRIES["MY"],
        "SG": NINTENDO_COUNTRIES["SG"],
    }

    print(f"\n将测试 {len(test_countries)} 个国家/地区:")
    for code, info in test_countries.items():
        print(f"  - {code}: {info['name']} ({info['currency']})")

    print("\n" + "=" * 80)
    print("开始测试...\n")

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(
            viewport={'width': 1920, 'height': 1080},
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        )
        page = await context.new_page()

        success_count = 0
        fail_count = 0

        for country_code, country_info in test_countries.items():
            print(f"[{country_code}] {country_info['name']}...")

            plans = await fetch_country_prices(page, country_code, country_info)

            if plans and len(plans) > 0:
                print(f"    OK - 成功抓取 {len(plans)} 个套餐")
                success_count += 1

                # 显示前3个套餐
                for i, plan in enumerate(plans[:3], 1):
                    print(f"      {i}. {plan.get('plan', 'Unknown')}: {plan.get('price', 'N/A')[:80]}")
            else:
                print("    FAIL - 未抓取到价格数据")
                fail_count += 1

            print()
            await asyncio.sleep(1)

        await browser.close()

        print("=" * 80)
        print("测试结果:")
        print(f"  成功: {success_count}/{len(test_countries)}")
        print(f"  失败: {fail_count}/{len(test_countries)}")

        if success_count == len(test_countries):
            print("\n所有测试通过！爬虫工作正常。")
            return True
        elif success_count > 0:
            print("\n部分测试通过。请检查失败的国家。")
            return True
        else:
            print("\n所有测试失败，请检查网络连接和页面结构。")
            return False


if __name__ == '__main__':
    result = asyncio.run(test_scraper())
    exit(0 if result else 1)
