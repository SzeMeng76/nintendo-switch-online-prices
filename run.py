#!/usr/bin/env python3
"""
Nintendo Switch Online 价���爬虫 - ���速���行脚本
���动运���爬虫���汇率转���
"""

import os
import sys
import subprocess


def check_requirements():
    """���查依赖是否安装"""
    print("���� 检���依赖...")

    try:
        import playwright
        import bs4
        import requests
        print("✅ 所有依赖已���装")
        return True
    except ImportError as e:
        print(f"❌ 缺少依���: {e}")
        print("\n请运行以下���令安装依赖:")
        print("  pip install -r requirements.txt")
        print("  playwright install chromium")
        return False


def check_api_key():
    """检查 API 密���是否配置"""
    print("\n���� 检查 API 密钥...")

    # 尝���从 .env 文件加载
    if os.path.exists('.env'):
        try:
            from dotenv import load_dotenv
            load_dotenv()
        except:
            pass

    api_key = os.getenv('API_KEY')

    if not api_key:
        print("❌ ���找��� API 密钥")
        print("\n���按以下���骤配置:")
        print("  1. 复制 .env.example ��� .env")
        print("  2. ��� .env ���添加你的 API_KEY")
        print("  3. 获取免��� API 密���: https://openexchangerates.org/")
        return False

    print(f"✅ API 密���已配置 (...{api_key[-4:]})")
    return True


def run_scraper():
    """运行爬虫"""
    print("\n" + "=" * 80)
    print("���� 步骤 1/2: 运行���格爬虫")
    print("=" * 80)

    result = subprocess.run([sys.executable, 'nintendo.py'])

    if result.returncode != 0:
        print("\n��� 爬虫运行失���")
        return False

    print("\n��� 爬���运���成功")
    return True


def run_converter():
    """运行汇率转���器"""
    print("\n" + "=" * 80)
    print("���� 步骤 2/2: ���换汇率���排序")
    print("=" * 80)

    result = subprocess.run([sys.executable, 'nintendo_rate_converter.py'])

    if result.returncode != 0:
        print("\n❌ ���率转换���败")
        return False

    print("\n✅ 汇率转换���功")
    return True


def main():
    print("���� Nintendo Switch Online ���格爬虫 - 快速���行")
    print("=" * 80)

    # 检���依���
    if not check_requirements():
        sys.exit(1)

    # 检查 API 密钥
    if not check_api_key():
        sys.exit(1)

    # ���行爬虫
    if not run_scraper():
        sys.exit(1)

    # 运行汇���转换
    if not run_converter():
        sys.exit(1)

    # 完成
    print("\n" + "=" * 80)
    print("���� 所���步骤完���！")
    print("\n���� 生成的文件:")
    print("  - nintendo_prices.json (原始数据)")
    print("  - nintendo_prices_cny_sorted.json (���序���的数据)")
    print("\n���� 提示:")
    print("  - 查��� nintendo_prices_cny_sorted.json ���的 _top_10_cheapest")
    print("  - 按人民币价格找到最便宜的订阅地���")
    print("=" * 80)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  用���中���")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n��� 发���错误: {e}")
        sys.exit(1)
