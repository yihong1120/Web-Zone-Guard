import torch
import os
from pathlib import Path
import json
from PIL import Image
import io
import time
import base64
from ultralytics.yolo.engine.predictor import BasePredictor
from ultralytics.yolo.engine.results import Results
from ultralytics.yolo.utils import DEFAULT_CFG, ROOT, ops


class_names = {
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


class DetectionPredictor(BasePredictor):
    def __init__(self, model_path, img_path, img_output, username, cfg=DEFAULT_CFG, use_python=False):
        super().__init__(overrides=dict(model=model_path, source=img_path))
        self.model_path = Path(model_path)
        self.img_path = Path(img_path)
        self.img_output = Path(img_output)
        self.username = username
        self.cfg = cfg
        self.use_python = use_python
        self.save_dir = self.img_output

        # Get the filename from self.img_path
        self.filename = os.path.basename(self.img_path)
        # Remove the extension from the filename
        self.filename_base, _ = os.path.splitext(self.filename)

        # Get the current timestamp in seconds
        timestamp = int(time.time())

        # Construct the directory path
        directory_path = Path('../records/history') / self.username

        # Create the directory if it does not exist
        directory_path.mkdir(parents=True, exist_ok=True)

        # Construct the full file path
        self.output_json_path = directory_path / f'{timestamp}_{self.filename_base}.json'

    def save_to_json(self, output_dict, output_json_path):
        """
        Save a dictionary to a JSON file.
        Args:
            output_dict (dict): The dictionary to be saved.
            output_json_path (str or Path): The path to save the JSON file.
        """
        with output_json_path.open('w') as f:
            json.dump(output_dict, f)

    def read_image_as_base64(self, image_path):
        """
        Read an image and return it as a base64 encoded string.
        Args:
            image_path (str or Path): The path to the image file.
        Returns:
            str: The base64 encoded image string.
        """
        with image_path.open('rb') as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')

    def postprocess(self, preds, img, orig_imgs):
        """
        Postprocesses predictions and returns a list of Results objects.
        Args:
            preds (Tensor): The predictions tensor.
            img (Tensor): The input image tensor.
            orig_imgs (Tensor or list[Tensor]): The original image tensor(s).
        Returns:
            list[Results]: The list of Results objects.
        """
        preds = ops.non_max_suppression(preds,
                                        self.args.conf,
                                        self.args.iou,
                                        agnostic=self.args.agnostic_nms,
                                        max_det=self.args.max_det,
                                        classes=self.args.classes)

        # # Get the filename from self.img_path
        # self.filename = os.path.basename(self.img_path)
        # # Remove the extension from the filename
        # self.filename_base, _ = os.path.splitext(self.filename)

        # Convert tensor to NumPy array
        array = img.numpy()

        self.yolo_resize_height = array.shape[2]
        self.yolo_resize_width = array.shape[3]

        # Convert NumPy array to PIL image
        image_pil = Image.fromarray(orig_imgs[0])

        # Create a BytesIO object and save the image as PNG
        byte_io = io.BytesIO()
        image_pil.save(byte_io, format='PNG')
        png_data = byte_io.getvalue()

        # Encode the byte data as base64
        base64_str = base64.b64encode(png_data).decode('utf-8')

        # Convert preds to a list so it can be serialized to JSON
        preds_list = preds[0].tolist()

        # Create a dictionary to save as JSON
        output_dict = {
            'filename': self.filename,
            'predictions': preds_list,
            'original_image': base64_str
        }

        self.save_to_json(output_dict, self.output_json_path)

        results = []
        for i, pred in enumerate(preds):
            orig_img = orig_imgs[i] if isinstance(orig_imgs, list) else orig_imgs
            if not isinstance(orig_imgs, torch.Tensor):
                pred[:, :4] = ops.scale_boxes(img.shape[2:], pred[:, :4], orig_img.shape)
            path = self.batch[0]
            img_path = path[i] if isinstance(path, list) else path
            results.append(Results(orig_img=orig_img, path=img_path, names=self.model.names, boxes=pred))

        return results

    def predict(self):
        """
        Runs YOLO model inference on input image(s).
        """
        if self.use_python:
            from ultralytics import YOLO
            YOLO(self.model_path)(**self.args)
        else:
            self.predict_cli()

            encoded_string = self.read_image_as_base64(self.img_output / self.filename)

            with self.output_json_path.open() as json_file:
                data = json.load(json_file)

            data['stream_inference_image'] = encoded_string
            self.save_to_json(data, self.output_json_path)

            os.remove(self.img_output / self.filename)


if __name__ == '__main__':
    detector = DetectionPredictor(model_path='models/yolov8x.pt', img_path='Tallinn.png', img_output='./output', username = 'arthurfr')
    detector.predict()
