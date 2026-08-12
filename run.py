#!/usr/bin/env python3
"""
Nintendo Switch Online 价格爬虫 - 快速运行脚本
自动运行爬虫和汇率转换
"""

import os
import sys
import subprocess


def check_requirements():
    """检查依赖是否安装"""
    print("检查依赖...")

    try:
        import playwright
        import bs4
        import requests
        print("OK - 所有依赖已安装")
        return True
    except ImportError as e:
        print(f"FAIL - 缺少依赖: {e}")
        print("\n请运行以下命令安装依赖:")
        print("  pip install -r requirements.txt")
        print("  playwright install chromium")
        return False


def check_api_key():
    """检查 API 密钥是否配置"""
    print("\n检查 API 密钥...")

    # 尝试从 .env 文件加载
    if os.path.exists('.env'):
        try:
            from dotenv import load_dotenv
            load_dotenv()
        except ImportError:
            pass

    api_key = os.getenv('API_KEY')

    if not api_key:
        print("FAIL - 未找到 API 密钥")
        print("\n请按以下步骤配置:")
        print("  1. 复制 .env.example 为 .env")
        print("  2. 在 .env 中添加你的 API_KEY")
        print("  3. 获取免费 API 密钥: https://openexchangerates.org/")
        return False

    print(f"OK - API 密钥已配置 (...{api_key[-4:]})")
    return True


def run_scraper():
    """运行爬虫"""
    print("\n" + "=" * 80)
    print("步骤 1/2: 运行价格爬虫")
    print("=" * 80)

    result = subprocess.run([sys.executable, 'nintendo.py'])

    if result.returncode != 0:
        print("\nFAIL - 爬虫运行失败")
        return False

    print("\nOK - 爬虫运行成功")
    return True


def run_converter():
    """运行汇率转换器"""
    print("\n" + "=" * 80)
    print("步骤 2/2: 转换汇率并排序")
    print("=" * 80)

    result = subprocess.run([sys.executable, 'nintendo_rate_converter.py'])

    if result.returncode != 0:
        print("\nFAIL - 汇率转换失败")
        return False

    print("\nOK - 汇率转换成功")
    return True


def main():
    print("Nintendo Switch Online 价格爬虫 - 快速运行")
    print("=" * 80)

    # 检查依赖
    if not check_requirements():
        sys.exit(1)

    # 检查 API 密钥
    if not check_api_key():
        sys.exit(1)

    # 运行爬虫
    if not run_scraper():
        sys.exit(1)

    # 运行汇率转换
    if not run_converter():
        sys.exit(1)

    # 完成
    print("\n" + "=" * 80)
    print("所有步骤完成！")
    print("\n生成的文件:")
    print("  - nintendo_prices.json (原始数据)")
    print("  - nintendo_prices_cny_sorted.json (排序后的数据)")
    print("\n提示:")
    print("  - 查看 nintendo_prices_cny_sorted.json 中的 _top_10_cheapest_individual_12month")
    print("  - 以及 _top_10_cheapest_family_12month")
    print("  - 按人民币价格找到最便宜的订阅地区")
    print("=" * 80)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n用户中断")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n发生错误: {e}")
        sys.exit(1)
