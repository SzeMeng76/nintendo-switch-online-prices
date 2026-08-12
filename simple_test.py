#!/usr/bin/env python3
import asyncio
from playwright.async_api import async_playwright
from bs4 import BeautifulSoup
import re


async def test_malaysia():
    url = "https://ec.nintendo.com/MY/en/membership"

    print("Nintendo Switch Online Price Test")
    print("=" * 80)
    print("Testing Country: Malaysia (MY)")
    print("URL:", url)
    print("=" * 80)

    async with async_playwright() as p:
        print("\nLaunching browser...")
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()

        print("Visiting page...")
        await page.goto(url, wait_until='domcontentloaded', timeout=30000)

        print("Waiting for page to render...")
        await page.wait_for_timeout(5000)

        print("Getting page content...")
        html = await page.content()

        with open('test_page.html', 'w', encoding='utf-8') as f:
            f.write(html)
        print("OK - Page HTML saved to test_page.html")

        soup = BeautifulSoup(html, 'html.parser')

        print("\nSearching for price information...")
        print("-" * 80)

        # Method 1: Find MYR or RM
        all_text = soup.get_text()
        myr_matches = re.findall(r'(MYR|RM)\s*[\d,\.]+|[\d,\.]+\s*(MYR|RM)', all_text, re.IGNORECASE)

        if myr_matches:
            print(f"\nOK - Found {len(myr_matches)} instances of MYR/RM:")
            for i, match in enumerate(myr_matches[:10], 1):
                print(f"   {i}. {match}")
        else:
            print("FAIL - No MYR or RM currency symbols found")

        # Method 2: Find elements with numbers
        print("\nSearching for elements with price patterns...")
        price_elements = soup.find_all(['div', 'span', 'p'], string=re.compile(r'[\d,]+'))

        print(f"OK - Found {len(price_elements)} elements with numbers")

        if price_elements:
            print("\nFirst 10 possible price elements:")
            for i, elem in enumerate(price_elements[:10], 1):
                text = elem.get_text(strip=True)
                if len(text) < 100:
                    print(f"   {i}. {text}")

        # Method 3: Find tables
        print("\nSearching for tables...")
        tables = soup.find_all('table')
        if tables:
            print(f"OK - Found {len(tables)} tables")
            for i, table in enumerate(tables, 1):
                print(f"\nTable {i}:")
                rows = table.find_all('tr')
                for j, row in enumerate(rows[:5], 1):
                    cols = [col.get_text(strip=True) for col in row.find_all(['td', 'th'])]
                    if cols:
                        print(f"   Row {j}: {' | '.join(cols)}")
        else:
            print("FAIL - No tables found")

        await browser.close()

        print("\n" + "=" * 80)
        print("OK - Test completed! Check test_page.html for full content")
        print("=" * 80)


if __name__ == '__main__':
    asyncio.run(test_malaysia())
