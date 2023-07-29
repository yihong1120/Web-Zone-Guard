import cv2
import ultralytics

class YOLOInference:
    def __init__(self, model_path):
        self.model = ultralytics.YOLO(model_path)

    def process_video(self, source):
        results = self.model(source, stream=True)

        for result in results:
            print(result.boxes.data)

    def process_image(self, source):
        results = self.model(source)  # not streaming for a single image
        detections = results[0].boxes.data
        orig_img = results[0].orig_img
        img_path = results[0].path

        return detections, orig_img, img_path

    @staticmethod
    def draw_boxes(image, detections, class_names):
        for detection in detections:
            x1, y1, x2, y2, confidence, class_id = detection
            class_name = class_names[int(class_id)]
            color = (0, 255, 0)  # Green color for the bounding box
            thickness = 2
            cv2.rectangle(image, (int(x1), int(y1)), (int(x2), int(y2)), color, thickness)
            label = f"{class_name}: {confidence:.2f}"
            cv2.putText(image, label, (int(x1), int(y1) - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
        return image

    @staticmethod
    def get_class_names():
        return {
            0: 'person', 1: 'bicycle', 2: 'car', 3: 'motorcycle', 4: 'airplane', 5: 'bus',
            6: 'train', 7: 'truck', 8: 'boat', 9: 'traffic light', 10: 'fire hydrant',
            11: 'stop sign', 12: 'parking meter', 13: 'bench', 14: 'bird', 15: 'cat',
            16: 'dog', 17: 'horse', 18: 'sheep', 19: 'cow', 20: 'elephant', 21: 'bear',
            22: 'zebra', 23: 'giraffe', 24: 'backpack', 25: 'umbrella', 26: 'handbag',
            27: 'tie', 28: 'suitcase', 29: 'frisbee', 30: 'skis', 31: 'snowboard',
            32: 'sports ball', 33: 'kite', 34: 'baseball bat', 35: 'baseball glove',
            36: 'skateboard', 37: 'surfboard', 38: 'tennis racket', 39: 'bottle',
            40: 'wine glass', 41: 'cup', 42: 'fork', 43: 'knife', 44: 'spoon', 45: 'bowl',
            46: 'banana', 47: 'apple', 48: 'sandwich', 49: 'orange', 50: 'broccoli',
            51: 'carrot', 52: 'hot dog', 53: 'pizza', 54: 'donut', 55: 'cake', 56: 'chair',
            57: 'couch', 58: 'potted plant', 59: 'bed', 60: 'dining table', 61: 'toilet',
            62: 'tv', 63: 'laptop', 64: 'mouse', 65: 'remote', 66: 'keyboard', 67: 'cell phone',
            68: 'microwave', 69: 'oven', 70: 'toaster', 71: 'sink', 72: 'refrigerator',
            73: 'book', 74: 'clock', 75: 'vase', 76: 'scissors', 77: 'teddy bear',
            78: 'hair drier', 79: 'toothbrush'
        }


if __name__ == '__main__':
    yolo_inference = YOLOInference('models/yolov8x.pt')
    # detections, orig_img = yolo_inference.process_image('Tallinn.png')
    
    # url = 'https://www.youtube.com/watch?v=z_mlibCfgFI&ab_channel=%E6%A1%83%E5%9C%92%E6%99%BA%E6%85%A7%E6%97%85%E9%81%8A%E9%9B%B2TaoyuanTravel'
    url = 'https://finnoytravel.com/images/Tallinn_Christmas_market_family_visitors.jpg'
    detections, orig_img = yolo_inference.process_image(url)

    image = yolo_inference.draw_boxes(orig_img, detections, YOLOInference.get_class_names())

    # Display the image
    cv2.imshow('Object Detection', image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
