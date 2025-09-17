import json
from datetime import datetime, timedelta
import os

# 加载当前和之前的结果
current_items = []
with open('latest_results.json', 'r') as f:
    for line in f:
        if line.strip():
            current_items.append(json.loads(line))

previous_items = []
if os.path.exists('previous_results_backup.json'):
    with open('previous_results_backup.json', 'r') as f:
        for line in f:
            if line.strip():
                previous_items.append(json.loads(line))

# 创建映射以便快速查找
previous_map = {item['html_url']: item for item in previous_items if 'html_url' in item}

updated_count = 0
updated_urls = []

for current in current_items:
    url = current.get('html_url')
    if not url:
        continue
        
    previous = previous_map.get(url)
    
    if previous:
        try:
            # 解析时间字符串
            current_updated = datetime.fromisoformat(current['updated_at'].replace('Z', '+00:00'))
            previous_updated = datetime.fromisoformat(previous['updated_at'].replace('Z', '+00:00'))
            
            # 检查是否在最近一次检查之后有更新
            if current_updated > previous_updated + timedelta(hours=1):
                # 检查其他重要变化
                star_increase = current.get('stargazers_count', 0) - previous.get('stargazers_count', 0)
                current_topics = set(current.get('topics', []))
                previous_topics = set(previous.get('topics', []))
                new_topics = current_topics - previous_topics
                
                # 如果有显著更新，则标记
                if (current_updated - previous_updated).days < 7 or star_increase > 2 or new_topics:
                    updated_count += 1
                    updated_urls.append(url)
                    print(f"检测到更新: {url}")
                    
        except (KeyError, ValueError) as e:
            print(f"处理项目 {url} 时出错: {e}")
            continue

# 保存更新列表
with open('updated_items.txt', 'w') as f:
    for url in updated_urls:
        f.write(f"{url}\n")

print(f"发现 {updated_count} 个项目有更新")