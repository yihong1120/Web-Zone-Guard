from urllib.parse import urlparse
import requests

def get_url_content_type(url):
    try:
        # 檢查網址是否有效
        response = requests.head(url)
        if not response.ok:
            return "Invalid URL"
        
        # 判斷是否為YouTube的URL
        if 'youtube' in url or 'youtu.be' in url:
            return "video"
            
        else:
            # 檢查網址的副檔名
            parsed = urlparse(url)
            ext = os.path.splitext(parsed.path)[1]
            image_exts = ['.png', '.jpg', '.jpeg', '.gif', '.bmp', '.webp', '.tiff']
            video_exts = ['.mp4', '.avi', '.mov', '.flv', '.wmv', '.mkv']
            if ext in image_exts:
                return "image"
            elif ext in video_exts:
                return "video"
            else:
                return "unknown"

    except (requests.exceptions.RequestException, Exception) as e:
        return str(e)
    
url = 'https://www.youtube.com/watch?v=z_mlibCfgFI&ab_channel=%E6%A1%83%E5%9C%92%E6%99%BA%E6%85%A7%E6%97%85%E9%81%8A%E9%9B%B2TaoyuanTravel'
print(get_url_content_type(url))