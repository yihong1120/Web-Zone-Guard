from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render
from django.views.decorators.http import require_POST
from django.http import JsonResponse, StreamingHttpResponse
from django.core.serializers.json import DjangoJSONEncoder
from django.views.decorators.csrf import csrf_exempt
from urllib.parse import urlparse
import base64
import json
import os
import requests
from PIL import Image
from io import BytesIO

from .yolov8 import YOLOInference

def index(request):
    allPredData = ["item1", "item2", "item3", "item4"]
    selectedPredData = ["item5", "item6", "item7", "item8"]
    shownPredData = {
    0: 'person', 1: 'bicycle', 2: 'car', 3: 'motorcycle', 5: 'bus',
    6: 'train', 7: 'truck'
    }

    allPredData_json = json.dumps(allPredData, cls=DjangoJSONEncoder)
    selectedPredData_json = json.dumps(selectedPredData, cls=DjangoJSONEncoder)
    
    if request.user.is_authenticated:
        return render(request, 'VisionSnap/logged_in.html', {
            'username': request.user.username, 
            'pred_class_names': YOLOInference.get_class_names(), 
            'allPredData':allPredData_json, 
            'selectedPredData':selectedPredData_json,
            'shownPredData': shownPredData,
            'process_url': '/process_url/',
        }) 
    else:
        form = AuthenticationForm()
        return render(request, 'accounts/login.html', {'form': form})
    
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

@csrf_exempt
def process_url(request):
    if request.method == 'POST':
        url = request.POST.get('url')
        print(url)
        content_type = get_url_content_type(url)
        yolo_inference = YOLOInference('models/yolov8x.pt')

        if content_type == 'image':
            print("oui, c'est une image.")

            # Image process
            detections, orig_img, img_path = yolo_inference.process_image(url)
            image = yolo_inference.draw_boxes(orig_img, detections, YOLOInference.get_class_names())

            # 將 numpy array 轉換為 PIL image
            image_pil = Image.fromarray(image)

            buffered = BytesIO()
            image_pil.save(buffered, format="JPEG")
            img_str = base64.b64encode(buffered.getvalue()).decode()
            os.remove(img_path)

            # 將 Base64 字串包裝在 JSON 物件中並返回到前端
            return JsonResponse({'status': 'success', 'image': img_str})

        elif content_type == 'video':
            print("c'est un vidéo.")

            def generate():
                for detections, orig_img in yolo_inference.process_video(url):
                    image = yolo_inference.draw_boxes(orig_img, detections, yolo_inference.get_class_names())
                    image_pil = Image.fromarray(image)

                    buffered = BytesIO()
                    image_pil.save(buffered, format="JPEG")
                    img_str = base64.b64encode(buffered.getvalue()).decode()
                    yield img_str

            return StreamingHttpResponse(generate(), content_type="image/jpeg")
            
    else:
        return JsonResponse({'status': 'failed'})

def controls(request):
    if request.user.is_authenticated:
        return render(request, 'VisionSnap/controls.html')
    else:
        form = AuthenticationForm()
        return render(request, 'accounts/login.html', {'form': form})