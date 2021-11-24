import cv2
import numpy as np
import time

def draw_bounding_box(img, class_id, confidence, x, y, x_plus_w, y_plus_h, classes):
    label = str(classes[class_id])
    label = "%s : %f" % (label, confidence)
    COLORS = [(0, 255, 255), (255, 255, 0), (0, 255, 0), (255, 0, 0)]
    color = COLORS[int(class_id) % len(COLORS)]
    cv2.rectangle(img, (x, y), (x_plus_w, y_plus_h), color, 2)
    cv2.putText(img, label, (x - 10, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

def draw_all_bounding_boxes(frame, boxes, class_ids, confidences, classes):
    for i in range(len(boxes)):
        x, y, w, h = boxes[i]
        draw_bounding_box(frame, class_ids[i], confidences[i], round(x), round(y), round(x + w), round(y + h), classes)

def build_model(classes_path='yolov4.txt', weights_path='yolov4.weights', config_path='yolov4.cfg'):
    with open(classes_path, 'r') as f:
        classes = [line.strip() for line in f.readlines()]
    net = cv2.dnn.readNet(weights_path, config_path)
    layer_names = net.getLayerNames()
    output_layers = [layer_names[i[0] - 1] for i in net.getUnconnectedOutLayers()]
    return net, classes, output_layers

def detect(net, frame, output_layers):
    class_ids = []
    confidences = []
    boxes = []
    CONFIDENCE_THRESHOLD = 0.5
    NMS_THRESHOLD = 0.4
    scale = 1/255
    size = (320, 320)
    blob = cv2.dnn.blobFromImage(frame, scalefactor=scale, size=size, mean=(0, 0, 0), swapRB=True, crop=False)
    net.setInput(blob)
    im_h, im_w = frame.shape[0:2]
    start = time.time()
    outs = net.forward(output_layers)
    end = time.time()
    for out in outs:
        for detection in out:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]
            if confidence > 0.5:
                center_x = int(detection[0] * im_w)
                center_y = int(detection[1] * im_h)
                w = int(detection[2] * im_w)
                h = int(detection[3] * im_h)
                x = center_x - w / 2
                y = center_y - h / 2
                class_ids.append(class_id)
                confidences.append(float(confidence))
                boxes.append([x, y, w, h])
    indices = cv2.dnn.NMSBoxes(boxes, confidences, CONFIDENCE_THRESHOLD, NMS_THRESHOLD)
    clean_class_ids = []
    clean_confidences = []
    clean_boxes = []
    for i in indices:
        j = i[0]
        clean_class_ids.append(class_ids[j])
        clean_boxes.append(boxes[j])
        clean_confidences.append(confidences[j])
    return clean_class_ids, clean_boxes, clean_confidences
