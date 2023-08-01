# 導入所需的模組
import requests
import cv2
import youtube_dl

# 設定直播影片網址
url = "https://www.youtube.com/watch?v=XntnzALjg1s&ab_channel=%E6%A0%AA%E5%BC%8F%E4%BC%9A%E7%A4%BE%E6%8A%80%E7%A0%94%E5%B7%A5%E6%88%BF"

# 使用youtube_dl模組獲取直播影片的m3u8格式的網址
ydl_opts = {}
with youtube_dl.YoutubeDL(ydl_opts) as ydl:
    info_dict = ydl.extract_info(url, download=False)
    formats = info_dict.get('formats',None)
    for f in formats:
        # 選擇最高畫質的m3u8網址
        if f.get('format_note',None) == '1440p':
            url = f.get('url',None)
            break

# 使用requests模組獲取m3u8檔案的內容
r = requests.get(url)
m3u8_content = r.text

# 從m3u8檔案的內容中找到最後一個ts檔案的網址
lines = m3u8_content.split("\n")
ts_url = None
for line in lines:
    if line.endswith(".ts"):
        ts_url = line
        break

# 如果找到了ts檔案的網址，則使用cv2模組讀取並儲存當前畫面
if ts_url is not None:
    # 拼接完整的ts檔案的網址
    ts_url = url.replace("playlist.m3u8",ts_url)
    # 讀取ts檔案並轉換為OpenCV可以處理的格式
    cap = cv2.VideoCapture(ts_url)
    ret, frame = cap.read()
    # 如果讀取成功，則儲存當前畫面為image.jpg檔案
    if ret:
        cv2.imwrite("image.jpg",frame)
        print("儲存成功")
    else:
        print("讀取失敗")
    # 釋放資源
    cap.release()
else:
    print("沒有找到ts檔案的網址")
