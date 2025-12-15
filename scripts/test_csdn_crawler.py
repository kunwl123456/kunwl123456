#!/usr/bin/env python3
"""
测试 CSDN 数据爬取（不修改 README）
"""

import requests
from bs4 import BeautifulSoup
import re

CSDN_URL = "https://blog.csdn.net/weixin_43679037"

def test_get_csdn_stats():
    """
    测试爬取 CSDN 数据
    """
    print(f"🔍 正在访问: {CSDN_URL}\n")
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }
    
    try:
        response = requests.get(CSDN_URL, headers=headers, timeout=10)
        response.raise_for_status()
        
        print(f"✅ HTTP 状态码: {response.status_code}")
        print(f"✅ 响应长度: {len(response.text)} 字符\n")
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # 打印页面标题
        title = soup.find('title')
        if title:
            print(f"📄 页面标题: {title.get_text(strip=True)}\n")
        
        # 查找所有可能包含数据的元素
        print("=" * 60)
        print("🔎 查找统计数据...")
        print("=" * 60)
        
        # 方法1: 查找包含数字的 data-info 元素
        data_infos = soup.select('.data-info')
        if data_infos:
            print(f"\n找到 {len(data_infos)} 个 .data-info 元素:")
            for i, elem in enumerate(data_infos, 1):
                print(f"  [{i}] {elem.get_text(strip=True)}")
        
        # 方法2: 查找个人成就卡片
        achievement_items = soup.select('.achievement-item, .user-profile-statistics-num')
        if achievement_items:
            print(f"\n找到 {len(achievement_items)} 个成就统计:")
            for i, elem in enumerate(achievement_items, 1):
                print(f"  [{i}] {elem.get_text(strip=True)}")
        
        # 方法3: 使用正则表达式查找所有包含数字的文本
        print("\n🔍 搜索关键词...")
        keywords = ['访问', '原创', '粉丝', '点赞', '排名', '获得']
        for keyword in keywords:
            matches = soup.find_all(text=re.compile(keyword))
            if matches:
                print(f"\n  含 '{keyword}' 的文本:")
                for match in matches[:3]:  # 只显示前3个
                    text = str(match).strip()
                    if text:
                        print(f"    - {text[:100]}")
        
        # 尝试提取具体数据
        print("\n" + "=" * 60)
        print("📊 尝试提取数据...")
        print("=" * 60)
        
        stats = {}
        
        # 访问量 - 多种尝试
        for selector in ['.data-info .data-value', '[title*="访问"]', '.profile-intro-name-left .count']:
            elem = soup.select_one(selector)
            if elem:
                text = elem.get_text(strip=True)
                numbers = re.findall(r'[\d,]+', text)
                if numbers:
                    stats['访问量'] = numbers[0]
                    break
        
        # 原创文章
        for selector in ['.data-info:nth-of-type(2) .data-value']:
            elem = soup.select_one(selector)
            if elem:
                text = elem.get_text(strip=True)
                numbers = re.findall(r'\d+', text)
                if numbers:
                    stats['原创'] = numbers[0]
                    break
        
        # 输出结果
        print()
        if stats:
            print("✅ 成功提取的数据:")
            for key, value in stats.items():
                print(f"  - {key}: {value}")
        else:
            print("⚠️ 未能提取到数据，可能需要调整选择器")
        
        print("\n" + "=" * 60)
        print("💡 提示:")
        print("  1. 如果数据提取失败，可能是 CSDN 页面结构改变")
        print("  2. 可以将完整 HTML 保存下来，手动分析元素结构")
        print("  3. 或者使用浏览器开发者工具查看元素 class/id")
        print("=" * 60)
        
        # 保存 HTML 用于调试
        debug_file = "/tmp/csdn_debug.html"
        with open(debug_file, 'w', encoding='utf-8') as f:
            f.write(response.text)
        print(f"\n📁 完整 HTML 已保存到: {debug_file}")
        print("   你可以用浏览器打开查看或用编辑器搜索关键词")
        
    except requests.RequestException as e:
        print(f"❌ 请求失败: {e}")
    except Exception as e:
        print(f"❌ 发生错误: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    print("=" * 60)
    print("🧪 CSDN 数据爬取测试工具")
    print("=" * 60)
    test_get_csdn_stats()
    print("\n✅ 测试完成！")

