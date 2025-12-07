import cv2
import numpy as np
from collections import Counter

"""
Online Sources Used
https://www.computervision.zone/courses/object-detection-mobile-net-ssd/?nsl_bypass_cache=00e43a010f43958bdabf63ca4b399085
https://www.askpython.com/resources/draw-bounding-boxes-image
https://github.com/opencv/opencv/wiki/TensorFlow-Object-Detection-API
"""



#Threshold & NMS Threshold (Reduce Duplication for same object detected)
thresh = 0.5
nms_threshold = 0.2

#File path to the image
#Change File to blob type for easier processing
img_file = "images/car-small-size.jpg"
img = cv2.imread(img_file)

#Stores the class names of the coco.names file
class_names = []
class_File = 'coco.names'

with open(class_File, 'rt') as f:
    class_names = f.read().rstrip('\n').split('\n')

print(class_names)



#Group Classes
CATEGORY_GROUPS = {
"vehicles": {"bicycle","car","motorcycle","bus","train","truck","boat","airplane"},
    "people": {"person"},
    "clothes_accessories": {"backpack","handbag","suitcase","tie","hat","eye glasses","shoe","umbrella"},
    "animals": {"bird","cat","dog","horse","sheep","cow","elephant","bear","zebra","giraffe"},
    "furniture": {"chair","couch","bed", "mirror","dining table","window", "desk","potted plant", "toilet", "door", "sink", "clock", "vase"},
    "food": {"banana","apple", "orange", "pizza","sandwich", "broccoli", "carrot", "hot dog", "donut", "cake"},
    "kitchen": {"bottle", "plate", "wine glass", "cup", "fork", "knife", "spoon", "bowl", "microwave","oven","toaster", "refrigerator", "blender"},
    "sports": {"sports ball","frisbee","kite","baseball bat","baseball glove","skateboard", "snowboard", "surfboard","tennis racket", "skis"},
    "street_items": {"traffic light","stop sign","parking meter","street sign","bench","fire hydrant"},
    "electronics": {"tv","laptop","cell phone","remote","keyboard","mouse"},
    "miscellaneous": {"hair drier", "toothbrush", "hairbrush", "teddy bear", "scissors"}
}

#map class names to their corresponding ids
name_to_id = {name.strip().lower(): i+1 for i, name in enumerate(class_names)}

#convert category groups to Id sets
group_to_ids = {}
for gname, names in CATEGORY_GROUPS.items():
    ids = {name_to_id[n.lower()] for n in names if n.lower() in name_to_id}
    group_to_ids[gname] = ids

#Where the user selects the groups
selected_groups = {"vehicles"}

#issue when none is selected, make sure to make the default all selected
#Need to handle the error when wrong items is detected or warn the user that an item may be wrongly detected
#Need to handle the error when no object can be detected in the image to provide warning no object could be detected
#Depending might need to use smaller image size to detect the object



#if categories are selected only allow those selected category ids

allowed_ids = set()
#When categories are selected on choose selected categories
if selected_groups:
    for g in selected_groups:
        allowed_ids |= group_to_ids.get(g, set())
#by default should allow all category ids
else:
    #default all groups is selected
    all_groups = {"vehicles", "people", "clothes_accessories", "animals", "furniture", "food", "kitchen", "sports", "street_items", "electronics", "miscellaneous" }
    for g in all_groups:
        allowed_ids |= group_to_ids.get(g, set())
    #allowed_ids = set(range(1, len(class_names) + 1))


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

#After Detection has been done

if len(classIds) == 0:
    print("No objects detected above confidence threshold")
else:
    #Convert classIds, confs, bbox to list for NMSBoxes
    bboxes_list = [list(map(int, b)) for b in bbox]
    confs_list = [float(c) for c in confs.flatten()]
    classIds_list = [int(classId) for classId in classIds.flatten()]

    #filter by allowed_ids Before NMS
    filtered = [
        (cid, confs_list[i], bboxes_list[i])
        for i, cid in enumerate(classIds_list)
        if cid in allowed_ids
    ]

    if not filtered:
        print("No objects from selected groups detected")
    else:
        #Create the boundary positions x,y,w,h for objects
        rects = [f[2] for f in filtered] # x, y, w, h
        scores = [f[1] for f in filtered] #confidence scores
        class_Ids = [f[0] for f in filtered] # class id

        #NMS returns indices of boxes to keep
        indices = cv2.dnn.NMSBoxes(rects, scores, thresh, nms_threshold)
        #normalize the list of lists returned by NMSBoxes

        if isinstance(indices, (list, tuple)) and len(indices) and isinstance(indices[0], (list, tuple, np.ndarray)):
            indices = [int(idx[0]) for idx in indices]
        elif isinstance(indices, np.ndarray):
            indices = indices.flatten().tolist()
        else:
            indices = [int(idx) for idx in indices]

        kept_class_ids = []
        #Draw the kept boxes and collect the counts
        for i in indices:
            x, y, w, h = rects[i]
            cid = class_Ids[i]
            score = scores[i]
            kept_class_ids.append(class_names[cid - 1])

            cv2.rectangle(img, (x, y), (x + w, y + h), color=(0, 255, 0), thickness=2)
            label = f"{class_names[cid - 1].upper()} {round(score * 100, 2)}%"
            cv2.putText(img, label, (x + 5, y + 25), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 2)

        #Total counts and counts per class
        total_count = len(kept_class_ids)
        per_class = Counter(kept_class_ids)

        print(f"Total objects detected: {total_count} objects")
        print(f"Counts per class:")
        for cls, cnt in per_class.items():
            print(f" {cls}: {cnt}")

#Print to check if all class ids exists, selected ids, and that class id each detected objects
print("class_names: length:", len(class_names))
print("allowed_ids (determined)", sorted((list(allowed_ids))[:len(allowed_ids)]))
#Hint at the items/class ids that were detected in the image if available, instead on no objects detected
print("Sample Detected class ids", classIds.flatten()[:len(classIds.flatten())])

cv2.imshow("picture",img)
cv2.waitKey(0)

# Working for detecting images
# for classId, confidence, box in zip(classIds.flatten(), confs.flatten(), bbox):
#     cv2.rectangle(img, box, color=(0, 255, 0), thickness=2)
#     cv2.putText(img, class_names[classId - 1].upper(), (box[0] + 10, box[1] + 30),
#                 cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 2)
#     cv2.putText(img, str(round(confidence * 100, 2)), (box[0] + 200, box[1] + 30),
#                 cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 2)

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



