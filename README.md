# ODIRA v1

### Object Detection Information Recording Application (ODIRA)

ODIRA is a full stack computer vision application designed to process images and record real time object classification analytics of them. The platform enables users to capture live images through webcam streams or static image files which returnes annotated results with bounding boxex, confidence scores and count of objects detected.

🌐 **Live Site:** [ODIRA](https://odira-object-detection-information.vercel.app/)

## Desktop Screenshots
<img width="780" height="872" alt="ODIRA Dashboard Top Section" src="https://github.com/user-attachments/assets/0aad175a-e818-4b4b-a20d-a01cc7fa97f6" />

<img width="803" height="535" alt="ODIRA Dashboard Bottom Section" src="https://github.com/user-attachments/assets/79b768cb-fd27-4dd5-8e13-b5491a08947c" />

<img width="637" height="768" alt="About Section" src="https://github.com/user-attachments/assets/5e01b701-0bad-46b6-b446-997b37e57794" />

## Mobile Screenshots
<img width="720" height="1600" alt="Screenshot_20260528-143701_Chrome" src="https://github.com/user-attachments/assets/f2cc9fec-b048-4daa-8bf7-85c260095d1b" />

<img width="720" height="1600" alt="Screenshot_20260528-143928_Chrome" src="https://github.com/user-attachments/assets/fc16a85b-251a-4394-bccd-b7037685672d" />




---

## Key Features

- **Granular Confidence Throttling:** Granular controls for Object Confidence and Non-Maximum Suppression (NMS) boundary-box overlapping calculations.
- **Class Filtering:** Category class toggle allows users to specify target object classes.
- **UI Feedback:** System feedback for user actions and analytics when finalizing resulting output of processed image.

---

## 💻 Tech Stack

- **Frontend:** Angular (v20.3.10), TypeScript (v5.8.3), Tailwind CSS, NGX-Webcam
- **Backend:** FastAPI, Python (v3.13), Pydantic (Data Validation), Starlette
- **Computer Vision:** OpenCV-Python (v4.12.0.88), MobileNet SSD v3 Model, COCO Dataset

---

## 🧠 Engineering Insights & Key Takeaways

Building ODIRA from scratch provided extensive experience in modern full stack data modeling and computer vision pipeline design:

- **Asynchronous Data:** Developed a custom JavaScript `FileReader` wrapper to encode local binary `File` objects into clean data URL strings, ensuring secure asynchronous transmission over REST APIs.
- **Reactive State Architecture:** Implemented modern Angular Signals (`signal`, `computed`, `effect`) combined with RxJS `BehaviorSubject` layers inside a singleton service context. This resolved an infinite rendering loop bug and isolated state mutations from presentation blueprints.
- **Computer Vision Optimization:** Configured a pre-trained MobileNet SSD engine to process image arrays, overlay color-coded boundary vectors, calculate class frequencies, and stream formatted analytics payloads back to the client.

---

## 🛠️ Lightweight Computer Vision Pipeline

1. **Pre-processing:** Takes the image frame and normalizes it to 320x320 scale and swaps RGB to BGR channel for OpenCV frame reading capability.
2. **Inference:** Uses the 'SSD-MobileNet-v3' model trained on the COCO dataset to extract raw bounding boxes and class confidence scores.
3. **Filtering & NMS:** Filters objects based on the UI class categories defined by the user and applies Non-Maximum Suppression (NMS) to eliminate duplicate detections.
4. **Annotation:** Scales bounding boxes and text, tracks object frequency and returns response JSON metadata.

---

## ⚙️ Installation & Local Development

### Prerequisites

- **Node.js** (v24.6.0+)
- **Python** (v3.13+)
- **PyCharm IDE** or **VS Code**

### 1. Clone the Repository

```bash
git clone https://github.com/Tony-Faijue/ODIRA-Object-Detection-Information-Recording-Application-.git
```

### 2. Launch the Angular Frontend

```bash
cd frontend/ODIRA
npm install
ng serve
```

_Navigate to `http://localhost:4200/` in your browser window._

### 3. Launch the Python/FastAPI Backend

```bash
cd backend/ODIRA
pip install fastapi opencv-python pydantic starlette apscheduler
fastapi dev odiraserver.py --port 9998
```

---

## 🌐 Network & Environment Configuration

To establish secure communication cross-origin pipelines locally you must declare explicit routing targets across both system layers.

### 1. Backend Server Layer (CORS Configuration)

Open the main API initialization entry-point file (e.g., `odiraserver.py`) and ensure that your Angular development server's domain origin port is explicitly whitelisted within the `CORSMiddleware` configuration array:

```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Declare local frontend cross-origin routes
origins = [
    "http://localhost:4200",  # Default local Angular Dev Server
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### 2. Frontend Client Layer (API Base URL Routing)

To direct your client form submissions, synchronize the dynamic image processing File_URL variable inside your Angular application service layer or your environment configuration to target your live running server instance port:

- **Local Pipeline Target:** `http://localhost:9998`

```typescript
// Create an environments folder and then a environment.ts file containing:
export const environment = {
    ProcessImageURL: 'http://127.0.0.1:9998'
}

//Or dircetly in process-image-service.ts

//---Replace This---
  private FILE_URL = `${environment.ProcessImageURL}/api/process-image`;

//---To This---
  private FILE_URL = `http://127.0.0.1:9998/api/process-image`;

```

Save changes and run both Angular and FastAPI again.

---

## 🐛 Bug Discovery & Issue Tracking

This is my first real project so any contributions, optimizations and feedback are highly encouraged. If you experience any unexpected errors or behaviors:

👉 [Open a Structured GitHub Issue Ticket](https://github.com/Tony-Faijue/ODIRA-Object-Detection-Information-Recording-Application-/issues)
