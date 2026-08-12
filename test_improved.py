#!/usr/bin/env python3
import asyncio
import json
from nintendo import fetch_country_prices, NINTENDO_COUNTRIES
from playwright.async_api import async_playwright


async def test_improved_scraper():
    country_code = "MY"
    country_info = NINTENDO_COUNTRIES[country_code]

    print("Nintendo Switch Online - Improved Scraper Test")
    print("=" * 80)
    print(f"Testing: {country_info['name']} ({country_code})")
    print("=" * 80)

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(
            viewport={'width': 1920, 'height': 1080},
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        )
        page = await context.new_page()

        print("\nFetching prices...")
        plans = await fetch_country_prices(page, country_code, country_info)

        await browser.close()

    print(f"\nResults: Found {len(plans)} plans")

    # Save to JSON file to avoid encoding issues
    output_file = 'test_result.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(plans, f, ensure_ascii=False, indent=2)

    print(f"Saved to: {output_file}")

    # Print summary without special characters
    print("\nSummary:")
    for i, plan in enumerate(plans, 1):
        print(f"  {i}. {plan['plan_type']} - {plan['duration_months']} months")

    print("\n" + "=" * 80)
    print("OK - Test completed! Check test_result.json for full details")


if __name__ == '__main__':
    asyncio.run(test_improved_scraper())
