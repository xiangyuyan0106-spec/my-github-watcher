import xml.etree.ElementTree as ET
from xml.dom import minidom
import datetime
import os

# 解析现有的RSS feed
rss_file = 'feed.xml'
if os.path.exists(rss_file):
    tree = ET.parse(rss_file)
    root = tree.getroot()
    channel = root.find('channel')
else:
    # 如果文件不存在，创建新的
    root = ET.Element('rss')
    root.set('version', '2.0')
    channel = ET.SubElement(root, 'channel')
    title = ET.SubElement(channel, 'title')
    title.text = 'GitHub Monitor: BYOVD & EDR Evasion'
    link = ET.SubElement(channel, 'link')
    link.text = f'https://github.com/{os.environ.get("GITHUB_REPOSITORY", "")}'
    description = ET.SubElement(channel, 'description')
    description.text = '监控BYOVD及EDR对抗项目的更新和新出现'
    language = ET.SubElement(channel, 'language')
    language.text = 'en-us'

# 解析新生成的items
rss_item_file = 'rss_items.xml'
if os.path.exists(rss_item_file):
    try:
        item_tree = ET.parse(rss_item_file)
        for item in reversed(item_tree.findall('item')):
            channel.insert(4, item)  # 在lastBuildDate之后插入
    except:
        pass

# 更新lastBuildDate
last_build_date = channel.find('lastBuildDate')
if last_build_date is None:
    last_build_date = ET.SubElement(channel, 'lastBuildDate')
last_build_date.text = datetime.datetime.now(datetime.timezone.utc).strftime('%a, %d %b %Y %H:%M:%S GMT')

# 保存文件
rough_string = ET.tostring(root, encoding='unicode')
parsed = minidom.parseString(rough_string)
with open(rss_file, 'w', encoding='utf-8') as f:
    f.write(parsed.toprettyxml(indent='  '))