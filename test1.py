import sys

import requests
from bs4 import BeautifulSoup
import os
sys
import time
import logging

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

print('百思不得姐图片爬取...')
# 注意：原网站可能已无法访问，这里使用示例URL用于演示
url = 'http://www.budejie.com/detail-27974418.html'
os.makedirs('bsbdj', exist_ok=True)

# 增加重试次数和更好的请求头
max_retries = 3
session = requests.Session()
session.headers.update({
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'Referer': 'http://www.budejie.com/',
})

statusValue = True
attempts = 0

while statusValue and attempts < max_retries:
    try:
        # 下载网页
        logger.info('Downloading page %s...', url)
        result = session.get(url, timeout=10)
        result.raise_for_status()
        
        soup = BeautifulSoup(result.text, "html.parser")
        
        # 查找图像 - 添加更灵活的选择器
        comicElem = soup.select('.j-r-list-c-img img')
        
        if not comicElem:
            # 尝试其他可能的选择器
            comicElem = soup.select('img')  # 回退方案
            if not comicElem:
                logger.warning('Could not find comic image elements')
                break
            logger.info('Found %d image elements using fallback selector', len(comicElem))
        
        # 下载图像
        comicUrl = comicElem[0].get('src')
        if not comicUrl.startswith('http'):
            comicUrl = 'http:' + comicUrl  # 处理相对URL
            
        logger.info('Downloading image %s...', comicUrl)
        
        # 下载图片时增加重试
        image_downloaded = False
        for img_attempt in range(max_retries):
            try:
                res = session.get(comicUrl, timeout=10, stream=True)
                res.raise_for_status()
                
                # 确保文件名有效
                img_filename = os.path.basename(comicUrl).split('?')[0]  # 移除URL参数
                imageFile = open(os.path.join('bsbdj', img_filename), 'wb')
                
                for chunk in res.iter_content(100000):
                    imageFile.write(chunk)
                
                imageFile.close()
                image_downloaded = True
                break
            except Exception as e:
                logger.error('Error downloading image: %s, attempt %d/%d', str(e), img_attempt + 1, max_retries)
                time.sleep(2)
        
        if not image_downloaded:
            logger.error('Failed to download image after %d attempts', max_retries)
            break
        
        # 查找下一页链接
        try:
            nextLink = soup.select('.c-next-btn-content .c-next-btn')[0]
            next_href = nextLink.get('href')
            if next_href:
                url = 'http://www.budejie.com' + next_href if not next_href.startswith('http') else next_href
            else:
                logger.info('No next page href found')
                break
        except (IndexError, AttributeError) as e:
            logger.error('Error finding next page: %s', str(e))
            break
        
        # 礼貌爬取，避免请求过快
        time.sleep(1)
        
    except requests.exceptions.RequestException as e:
        attempts += 1
        logger.error('Request error: %s, attempt %d/%d', str(e), attempts, max_retries)
        if attempts < max_retries:
            logger.info('Retrying in 3 seconds...')
            time.sleep(3)
        else:
            logger.error('Failed after %d attempts', max_retries)
            break
    except Exception as e:
        logger.error('Unexpected error: %s', str(e))
        break

# 爬图结束
print('Done...')