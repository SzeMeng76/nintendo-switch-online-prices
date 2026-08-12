#!/usr/bin/env python3
"""
Nintendo Switch Online 价格爬���测���脚���
快速���试几个���家的价格抓取是否���常
"""

import asyncio
from nintendo import fetch_country_prices, NINTENDO_COUNTRIES
from playwright.async_api import async_playwright


async def test_scraper():
    """���试爬���功能"""
    print("���� Nintendo Switch Online 爬���测试")
    print("=" * 80)

    # 选择���个代表���国���进行测试
    test_countries = {
        "US": NINTENDO_COUNTRIES["US"],
        "JP": NINTENDO_COUNTRIES["JP"],
        "MY": NINTENDO_COUNTRIES["MY"],
        "SG": NINTENDO_COUNTRIES["SG"],
    }

    print(f"\n📋 ���测试 {len(test_countries)} 个���家/地区:")
    for code, info in test_countries.items():
        print(f"  - {code}: {info['name']} ({info['currency']})")

    print("\n" + "=" * 80)
    print("🚀 ���始测试...\n")

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
            print(f"📍 [{country_code}] {country_info['name']}...")

            plans = await fetch_country_prices(page, country_code, country_info)

            if plans and len(plans) > 0:
                print(f"    ✅ 成功抓取 {len(plans)} 个套餐")
                success_count += 1

                # ���示前3个套���
                for i, plan in enumerate(plans[:3], 1):
                    print(f"      {i}. {plan.get('plan', 'Unknown')}: {plan.get('price', 'N/A')}")
            else:
                print(f"    ❌ ���抓取到价���数据")
                fail_count += 1

            print()
            await asyncio.sleep(1)

        await browser.close()

        print("=" * 80)
        print("📊 测试结果:")
        print(f"  ✅ 成功: {success_count}/{len(test_countries)}")
        print(f"  ❌ 失败: {fail_count}/{len(test_countries)}")

        if success_count == len(test_countries):
            print("\n🎉 所有测���通过！���虫工作正常。")
            return True
        elif success_count > 0:
            print("\n⚠️  ���分测���通过。请检���失败的国家。")
            return True
        else:
            print("\n❌ ���有测���失败���请检���网���连接和页面结���。")
            return False


if __name__ == '__main__':
    result = asyncio.run(test_scraper())
    exit(0 if result else 1)
