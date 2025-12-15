#!/usr/bin/env python3
"""
自动更新 CSDN 统计数据到 GitHub Profile README
"""

import re
import requests
from bs4 import BeautifulSoup

# CSDN 博客地址
CSDN_URL = "https://blog.csdn.net/weixin_43679037"

# README 文件路径（相对于 scripts 目录的上一级）
import os
README_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "README.md")

def get_csdn_stats():
    """
    爬取 CSDN 统计数据
    """
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    
    try:
        response = requests.get(CSDN_URL, headers=headers, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        
        stats = {}
        
        # 使用正确的选择器获取统计数据
        # 获取所有统计数字元素
        stat_nums = soup.select('.user-profile-statistics-num')
        stat_names = soup.select('.user-profile-statistics-name')
        
        # 遍历并匹配数据
        for num_elem, name_elem in zip(stat_nums, stat_names):
            num_text = num_elem.get_text(strip=True)
            name_text = name_elem.get_text(strip=True)
            
            # 提取数字（去除逗号）
            num_match = re.search(r'([\d,]+)', num_text)
            if num_match:
                value = int(num_match.group(1).replace(',', ''))
                
                # 根据名称映射到对应的键
                if '访问' in name_text:
                    stats['views'] = value
                elif '原创' in name_text:
                    stats['articles'] = value
                elif '粉丝' in name_text:
                    stats['fans'] = value
        
        # 获取点赞数（在个人成就部分）
        likes_elem = soup.find('div', class_='aside-common-box-content-text')
        if likes_elem:
            likes_text = likes_elem.get_text(strip=True)
            likes_match = re.search(r'获得[<>spn/]*?([\d,]+)', likes_text)
            if likes_match:
                stats['likes'] = int(likes_match.group(1).replace(',', ''))
        
        # 获取排名（在 achievementList 数据中或页面文本）
        rank_elem = soup.find(string=re.compile('博客总排名'))
        if rank_elem:
            # 查找紧邻的包含数字的元素
            parent = rank_elem.find_parent()
            if parent:
                rank_text = parent.get_text()
                rank_match = re.search(r'(\d[\d,]*)', rank_text)
                if rank_match:
                    stats['rank'] = int(rank_match.group(1).replace(',', ''))
        
        print(f"✅ 成功获取 CSDN 数据: {stats}")
        return stats
        
    except Exception as e:
        print(f"❌ 获取 CSDN 数据失败: {e}")
        return None

def update_readme(stats):
    """
    更新 README 文件中的统计数据
    """
    if not stats:
        print("⚠️ 没有可用的统计数据，跳过更新")
        return False
    
    try:
        with open(README_PATH, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 更新访问量
        if 'views' in stats:
            content = re.sub(
                r'{"博客访问量", \d+}',
                f'{{"博客访问量", {stats["views"]}}}',
                content
            )
        
        # 更新原创文章数
        if 'articles' in stats:
            content = re.sub(
                r'{"原创文章", \d+}',
                f'{{"原创文章", {stats["articles"]}}}',
                content
            )
        
        # 更新排名
        if 'rank' in stats:
            content = re.sub(
                r'{"CSDN排名", \d+}',
                f'{{"CSDN排名", {stats["rank"]}}}',
                content
            )
        
        # 更新点赞数
        if 'likes' in stats:
            content = re.sub(
                r'{"获得点赞", \d+}',
                f'{{"获得点赞", {stats["likes"]}}}',
                content
            )
        
        # 写回文件
        with open(README_PATH, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print("✅ README 更新成功！")
        return True
        
    except Exception as e:
        print(f"❌ 更新 README 失败: {e}")
        return False

def main():
    print("🚀 开始更新 CSDN 统计数据...")
    stats = get_csdn_stats()
    
    if stats:
        update_readme(stats)
        print("🎉 完成！")
    else:
        print("⚠️ 未能获取统计数据")

if __name__ == '__main__':
    main()

