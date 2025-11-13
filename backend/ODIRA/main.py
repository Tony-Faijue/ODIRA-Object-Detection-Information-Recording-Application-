import cv2
import numpy as np

#Threshold & NMS Threshold (Reduce Duplication for same object detected)
thresh = 0.5
nms_threshold = 0.2

#File path to the image
#Change File to blob type for easier processing
img_file = "images/The Rock.jpg"
img = cv2.imread(img_file)

#Stores the class names of the coco.names file
class_names = []
class_File = 'coco.names'

with open(class_File, 'rt') as f:
    class_names = f.read().rstrip('\n').split('\n')

print(class_names)

#Weights & Configurations
configPath = "ssd_mobilenet_v3_large_coco_2020_01_14.pbtxt"
weightsPath = "frozen_inference_graph.pb"

#Create the model with the config and weights
net = cv2.dnn_DetectionModel(weightsPath, configPath)

#default configurations
net.setInputSize(320, 320)
net.setInputScale(1.0/127.5)
net.setInputMean(127.5)
net.setInputSwapRB(True)

classIds, confs, bbox = net.detect(img, confThreshold=thresh)


if len(classIds) != 0:
    for classId, confidence, box in zip(classIds.flatten(), confs.flatten(), bbox):
        cv2.rectangle(img, box, color=(0, 255, 0), thickness=2)
        cv2.putText(img, class_names[classId - 1].upper(), (box[0] + 10, box[1] + 30),
                    cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 2)
        cv2.putText(img, str(round(confidence * 100, 2)), (box[0] + 200, box[1] + 30),
                    cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 2)

cv2.imshow("picture",img)
cv2.waitKey(0)


# #Convert these list to remove the reliance on numpy types
# bbox = list(bbox)
# confs = list(np.array(confs).reshape(1, -1)[0]) #except this one
# confs = list(map(float, confs))

# indices = cv2.dnn.NMSBoxes(bbox, confs, thresh, nms_threshold=nms_threshold)
# for i in indices:
#     box = bbox[i]
#     x,y,w,h = box[0], box[1], box[2], box[3]
#     cv2.rectangle(img, (x, y), (x + w, y + h), color=(0, 255, 0), thickness=2)
#     cv2.putText(img, class_names[classIds[i] - 1].upper(), (box[0] + 10, box[1] + 30),
#                 cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 2)
#     cv2.putText(img, str(round(confidence * 100, 2)), (box[0] + 200, box[1] + 30),
#                 cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 2)
#



