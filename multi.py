import glob
import cv2
import os
from src import ocr
import argparse
from src.detector import build_model, detect
from src.cleaner import process_image
from src.utils import display_image, resize
from src.json_dump import json_dump

path = glob.glob("multi-input/*.jpg")
cv_img = []
for img in path:
    n = cv2.imread(img)
    cv_img.append(n)
    cv2.imwrite("process/input.jpg", n)

    def argument_parser():
        ap = argparse.ArgumentParser()
        ap.add_argument('-i', '--image', default='process/input.jpg')
        ap.add_argument('-c', '--config', default='yolov4.cfg')
        ap.add_argument('-w', '--weights', default='yolov4.weights')
        ap.add_argument('-cl', '--classes', default='yolov4.txt')
        args = vars(ap.parse_args())
        return args

    def get_code(frame, class_ids, classes, boxes, debug=False):
        n_obj = len(class_ids)
        codes = []
        for i in range(n_obj):
            x, y, w, h = boxes[i]
            extra_pix = 2
            crop_img = frame[round(y)-extra_pix:round(y+h)+extra_pix, round(x)-extra_pix:round(x+w)+extra_pix]
            if crop_img.shape[0] == 0 or crop_img.shape[1] == 0:
                continue
            crop_img = resize(crop_img)
            # if debug:
            #     display_image(crop_img, "cropped code image")
            clean_img = process_image(crop_img, debug)
            clean_img = cv2.bitwise_not(clean_img)
            clean_img = cv2.blur(clean_img, (2, 2))
            res = ocr.find_code(clean_img)
            print("Detected code:", res)
            codes.append(res)
            # if debug:
            #     display_image(clean_img, "cleaned code image")
            json_dump(res)
            os.remove("process/input.jpg")
        return frame, codes

    def main(args):
        src_img = cv2.imread(args['image'])
        net, classes, output_layers = build_model(args['classes'], args['weights'], args['config'])
        class_ids, boxes, confidences = detect(net, src_img, output_layers)
        src_img, _ = get_code(src_img, class_ids, classes, boxes, debug=True)

    if __name__ == "__main__":
        argument = argument_parser()
        main(argument)   

path = glob.glob("multi-input/*.png")
cv_img = []
for img in path:
    n = cv2.imread(img)
    cv_img.append(n)
    cv2.imwrite("process/input.png", n)

    def argument_parser():
        ap = argparse.ArgumentParser()
        ap.add_argument('-i', '--image', default='process/input.png')
        ap.add_argument('-c', '--config', default='yolov4.cfg')
        ap.add_argument('-w', '--weights', default='yolov4.weights')
        ap.add_argument('-cl', '--classes', default='yolov4.txt')
        args = vars(ap.parse_args())
        return args

    def get_code(frame, class_ids, classes, boxes, debug=False):
        n_obj = len(class_ids)
        codes = []
        for i in range(n_obj):
            x, y, w, h = boxes[i]
            extra_pix = 2
            crop_img = frame[round(y)-extra_pix:round(y+h)+extra_pix, round(x)-extra_pix:round(x+w)+extra_pix]
            if crop_img.shape[0] == 0 or crop_img.shape[1] == 0:
                continue
            crop_img = resize(crop_img)
            # if debug:
            #     display_image(crop_img, "cropped code image")
            clean_img = process_image(crop_img, debug)
            clean_img = cv2.bitwise_not(clean_img)
            clean_img = cv2.blur(clean_img, (2, 2))
            res = ocr.find_code(clean_img)
            print("Detected code:", res)
            codes.append(res)
            # if debug:
            #     display_image(clean_img, "cleaned code image")
            json_dump(res)
            os.remove("process/input.png")
        return frame, codes

    def main(args):
        src_img = cv2.imread(args['image'])
        net, classes, output_layers = build_model(args['classes'], args['weights'], args['config'])
        class_ids, boxes, confidences = detect(net, src_img, output_layers)
        src_img, _ = get_code(src_img, class_ids, classes, boxes, debug=True)

    if __name__ == "__main__":
        argument = argument_parser()
        main(argument)   