from contextlib import asynccontextmanager

from apscheduler.schedulers.background import BackgroundScheduler
from fastapi import FastAPI, HTTPException, File, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field
from starlette.status import HTTP_201_CREATED
import cv2
import numpy as np
import os
import time
import uuid
from collections import Counter

"""
Online Sources Used
https://eranfeit.net/ssd-mobilenet-v3-object-detection-explained-for-beginners/
https://docs.opencv.org/3.4/d6/d0f/group__dnn.html 
https://www.computervision.zone/courses/object-detection-mobile-net-ssd/?nsl_bypass_cache=00e43a010f43958bdabf63ca4b399085
https://www.askpython.com/resources/draw-bounding-boxes-image
https://www.youtube.com/watch?v=rvFsGRvj9jo
https://www.geeksforgeeks.org/python/create-a-directory-in-python/
https://fastapi.tiangolo.com/advanced/custom-response/#fileresponse
"""

"""
--------Fast API Setup---------
Manages the server initialization and basic configurations
"""

"""
Sources Used for apscheduler, aysnccontextmanager, OS time
https://apscheduler.readthedocs.io/en/3.x/userguide.html
https://fastapi.tiangolo.com/advanced/events/#startup-and-shutdown-together
https://www.blog.pythonlibrary.org/2013/11/14/python-101-how-to-write-a-cleanup-script/
"""

#Method to delete files older than 10 minutes in the directory every 5 minutes
def clean_up_files():
    now = time.time()
    for filename in os.listdir(PROCESSED_IMAGE_DIR):
        file_path = os.path.join(PROCESSED_IMAGE_DIR, filename)
        #Check if file older than 10 minutes
        if os.stat(file_path):
            if os.stat(file_path).st_mtime < now - 600:
                try:
                    os.remove(file_path)
                except Exception as e:
                    print(f"Error deleting {filename}: {e}")

#Background Task Scheduling To Handle Cleaning/Deleting Images Every 5 minutes on the server
@asynccontextmanager
async def lifespan(app: FastAPI):
    scheduler = BackgroundScheduler()
    #Intialize the scheduler and jobs before the server starts
    scheduler.add_job(clean_up_files,'interval', minutes=5)
    scheduler.start()
    yield
    #Shutdown the scheduler when the server ends
    scheduler.shutdown()

app = FastAPI(lifespan=lifespan)

#To run server
# fastapi dev odiraserver.py --port 9998
origins = [
    #Local Testing
    # "http://localhost:4200",
    # "http://127.0.0.1:9998",
    #Vercel URLs
    "https://odira-object-detection-information.vercel.app",
    "https://liable-puffin-faijuetony-7847542b.koyeb.app"

]
#Middleware for Routes
app.add_middleware(CORSMiddleware, allow_origins=origins, allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

#Source for creating a directory
#: https://www.geeksforgeeks.org/python/create-a-directory-in-python/


#Store the new processed images in a local directory
PROCESSED_IMAGE_DIR = "processed_images"
os.makedirs(PROCESSED_IMAGE_DIR, exist_ok=True)

#References used for setting FASTAPI endpoints
#: https://www.youtube.com/watch?v=rvFsGRvj9jo


"""
Response Object To Return
Pydantic model defining the JSON data returned to Angular
"""
class ImageFile(BaseModel):
    image_file_id: str = Field(..., description="ID of the processed image")
    content_type: str = Field(..., description="MIME type")
    file_name: str = Field(..., description="Original filename")
    results: list = Field(..., description="List of items Detected, Count per item, Total Count of Items")
    image_url: str = Field(..., description="URL to retrieve processed image")

"""
Pydantic models for settings data validation
Models define the expected structure of the JSON string sent from Angular
"""
class CategorySetting(BaseModel):
    id:str
    name:str
    checked:bool
    label:str

class SettingsData(BaseModel):
    objThresh:float
    nmsThresh:float
    categories: list[CategorySetting]

"""
--------Object Detection SetUp---------
Loads configuration files and initializes the OpenCV DNN Model with SSD MobileNet v3
"""

#Source used for Object Threshold Setup: https://eranfeit.net/ssd-mobilenet-v3-object-detection-explained-for-beginners/

#Store the class names from the coco names file
class_names = []
class_File = 'coco.names'

with open(class_File, 'rt') as f:
    class_names = f.read().rstrip('\n').split('\n')

#Group Classes into categories
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
    "miscellaneous": {"hair drier", "toothbrush", "hair brush", "teddy bear", "scissors", "book"}
}
# Logic to assign ids to each category and ids for each item/name per category

#map the class name to the corresponding id
name_to_id = {name.strip().lower(): i+1 for i, name in enumerate(class_names)}

#Convert category groups to id sets
group_to_ids = {}
for gname, names in CATEGORY_GROUPS.items():
    ids = {name_to_id[n.lower()] for n in names if n.lower() in name_to_id}
    group_to_ids[gname] = ids


#Weights & Configurations for pretrained object detection model
configPath = "ssd_mobilenet_v3_large_coco_2020_01_14.pbtxt"
weightsPath = "frozen_inference_graph.pb"

#Create the model with the config and weights
net = cv2.dnn_DetectionModel(weightsPath, configPath)

#default configurations
net.setInputSize(320, 320)
net.setInputScale(1.0/127.5)
net.setInputMean(127.5)
net.setInputSwapRB(True)

"""
Method to return info about objects detected and image
"""
def detect_objects_from_image(img, settings_data_model:SettingsData):
    """
    Method to perform object detection when given an image and setting for thresholds and categories
    :param img:
    :param settings_data_model: the settings that contains thresholds and categories
    :return: results list and modified image array
    """
    #Access the thresholds/confidence from the pydantic model
    thresh = settings_data_model.objThresh
    nms_threshold = settings_data_model.nmsThresh


    #Determine which class Ids are allowed based on the user's checked category groups
    allowed_ids = set()
    for category in settings_data_model.categories:
        if category.checked:
            #Add all the item Ids belonging to checked category group
            category_group_ids = group_to_ids.get(category.name)
            if category_group_ids:
                allowed_ids.update(category_group_ids)

    #Sources used for drawing boundary boxes and implementing detection
    #: https://www.computervision.zone/courses/object-detection-mobile-net-ssd/?nsl_bypass_cache=00e43a010f43958bdabf63ca4b399085
    #: https://www.askpython.com/resources/draw-bounding-boxes-image

    #Perform detection using the confidence threshold
    classIds, confs, bbox = net.detect(img, confThreshold=thresh)

    #Convert classids, confs, bbox to flat lists for NMS Boxes compatibility
    if len(classIds) > 0:
        # Convert classIds, confs, bbox to list for NMSBoxes
        bboxes_list = [list(map(int, b)) for b in bbox]
        confs_list = [float(c) for c in confs.flatten()]
        classIds_list = [int(classId) for classId in classIds.flatten()]

        # filter by allowed_ids Before NMS
        filtered = [
            (cid, confs_list[i], bboxes_list[i])
            for i, cid in enumerate(classIds_list)
            if cid in allowed_ids
        ]

        if not filtered:
            return [], img
        else:
            # Create the boundary positions x,y,w,h for objects
            rects = [f[2] for f in filtered]  # x, y, w, h
            scores = [f[1] for f in filtered]  # confidence scores
            class_Ids = [f[0] for f in filtered]  # class id

            # NMS returns indices of boxes to keep, using the nms thresh
            indices = cv2.dnn.NMSBoxes(rects, scores, thresh, nms_threshold)
            # normalize the list of lists returned by NMSBoxes

            if isinstance(indices, (list, tuple)) and len(indices) and isinstance(indices[0],(list, tuple, np.ndarray)):
                indices = [int(idx[0]) for idx in indices]
            elif isinstance(indices, np.ndarray):
                indices = indices.flatten().tolist()
            else:
                indices = [int(idx) for idx in indices]

            kept_class_ids = [] #list of names of kept classes after NMS

            # Draw the kept boxes and collect the counts
            for i in indices:
                x, y, w, h = rects[i]
                cid = class_Ids[i]
                score = scores[i]
                class_name = class_names[cid - 1]
                kept_class_ids.append(class_names[cid - 1])

                cv2.rectangle(img, (x, y), (x + w, y + h), color=(0, 255, 0), thickness=2)
                label = f"{class_name.upper()} {round(score * 100, 2)}%"

                font = cv2.FONT_HERSHEY_COMPLEX_SMALL
                font_scale = 1
                font_thickness = 1

                (text_width, text_height), baseline = cv2.getTextSize(label, font, font_scale, font_thickness)

                while text_width > w - 10 and font_scale > 0.1:
                    font_scale -= 0.05
                    (text_width, text_height), baseline = cv2.getTextSize(label, font, font_scale, font_thickness)

                label_y_pos = y - 10 if y - 10 > 10 else y + text_height + 10

                cv2.putText(img, label, (x + 5, label_y_pos), font, font_scale, (0, 255, 0), font_thickness, cv2.LINE_AA)

            # Total counts and counts per class
            total_count = len(kept_class_ids)
            per_class = Counter(kept_class_ids)

            #Format the results into a list of dictionaries
            results_list = [
                {"item":cls, "count":cnt, "total_count_of_objects":total_count}
            for cls, cnt in per_class.items()
            ]
            return results_list, img
    else: #No detections found
        return [], img

"""
Method to handle image upload, processing and JSON response
POST endpoint
"""
@app.post("/api/process-image", response_model=ImageFile, status_code=HTTP_201_CREATED)
async def process_image_upload(file: UploadFile = File(...), settings: str = Form(...)):

    #Parse the JSON settings string into validated Pydantic model
    try:
        settings_data_model = SettingsData.model_validate_json(settings)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid settings data provided: {e}")

    #Convert the uploaded file into numpy array for cv2
    contents = await file.read()
    np_array = np.frombuffer(contents, np.uint8)
    img = cv2.imdecode(np_array, cv2.IMREAD_COLOR)

    if img is None:
        raise HTTPException(status_code=400, detail="Could not decode image file.")

    #Process the image, with passing the settings model
    #Returns the count of total objects detected, items and counts per item along with image with drawn boxes
    results_data, processed_img = detect_objects_from_image(img, settings_data_model)

    #Generate unique img id using the current time
    image_id = str(uuid.uuid4())
    save_path = os.path.join(PROCESSED_IMAGE_DIR, f"{image_id}.png")
    #Save the processed image to disk with unique id
    cv2.imwrite(save_path, processed_img)

    base_url = "http://127.0.0.1:9998"

    response_object = ImageFile(
        image_file_id=image_id,
        content_type="image/png",
        file_name=file.filename,
        results=results_data,
        image_url=f"{base_url}/api/image/{image_id}"
    )
    return response_object

"""
Method to return the processed image
GET Endpoint, returns raw image bytes
"""
@app.get("/api/image/{image_file_id}")
async def get_processed_image(image_file_id: str):
    #Source for adding to created directory
    #: https://fastapi.tiangolo.com/advanced/custom-response/#fileresponse

    file_path = os.path.join(PROCESSED_IMAGE_DIR, f"{image_file_id}.png")

    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="Processed image not found.")
    #Return the process image file
    return FileResponse(path=file_path, media_type="image/png")
