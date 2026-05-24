# ODIRA v1 🎯

### Object Detection Information Recording Application

ODIRA is a production-grade, full-stack computer vision application designed to process, and record real-time object classification analytics. Leveraging a standalone architecture, the platform enables users to capture live images through webcam streams or static media files to extract bounding-box metadata and instance metrics via an asynchronous intelligence pipeline.

🌐 **Live Demo Canvas:** [ODIRA](https://odira-object-detection-information.vercel.app/)

---

## 🏛️ System Architecture Workflow

### Key Engineering Capabilities

- **Granular Confidence Throttling:** Real-time adjustments for Object Confidence and Non-Maximum Suppression (NMS) boundary-box overlapping calculations.
- **Deterministic Class Filtering:** Non-destructive category toggles allowing users to scope analytics to specific target object matrix classes safely.
- **Unified UI Feedback System:** Real-time breathing neon visual status anchors providing instant confirmation of asset pipeline readiness.

---

## 💻 Tech Stack

### Core Engineering Layer

- **Frontend Ecosystem:** Angular (v20.3.10), TypeScript (v5.8.3), Tailwind CSS, NGX-Webcam
- **Backend Infrastructure:** FastAPI, Python (v3.13), Pydantic (Data Validation), Starlette
- **Computer Vision Core:** OpenCV-Python (v4.12.0.88), MobileNet SSD v3 Model, COCO Dataset

---

## 🧠 Engineering Insights & Key Takeaways

Building ODIRA from scratch provided extensive experience in modern full-stack data modeling and computer vision pipeline design:

- **Asynchronous Data:** Developed a custom JavaScript `FileReader` wrapper to encode local binary `File` objects into clean data URL strings, ensuring secure asynchronous transmission over REST boundaries.
- **Reactive State Architecture:** Implemented modern Angular Signals (`signal`, `computed`, `effect`) combined with RxJS `BehaviorSubject` layers inside a singleton service context. This resolved an infinite rendering rendering loop bug and isolated state mutations from presentation blueprints.
- **Computer Vision Optimization:** Configured a pre-trained MobileNet SSD engine to process image arrays, overlay color-coded boundary vectors, calculate class frequencies, and stream formatted analytics payloads back to the client container.

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
cd ../../backend/ODIRA
pip install fastapi opencv-python pydantic starlette apscheduler
fastapi dev odiraserver.py --port 9998
```

---

## 🌐 Network & Environment Configuration

To establish secure communication cross-origin pipelines locally you must declare explicit routing targets across both system layers.

### 1. Backend Server Layer (CORS Configuration)

Open your main API initialization entry-point file (e.g., `odiraserver.py`) and ensure that your Angular development server's domain origin port is explicitly whitelisted within the `CORSMiddleware` configuration array:

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

To direct your client form submissions to the proper execution thread environment, synchronize the dynamic image processing URL variable inside your Angular application service layer (or your component configuration endpoints) to target your live running server instance port:

- **Local Pipeline Target:** `http://localhost:9998`

```typescript
// Inside your Angular client application endpoint configuration
public readonly apiBaseUrl = 'http://localhost:9998'; // Points cleanly to your server execution framework port
public readonly processImageUrl = `${this.apiBaseUrl}/process-image`;
```

---

## 🐛 Bug Discovery & Issue Tracking

Contributions and optimization feedback are highly encouraged. If you experience unexpected layout behavior or inference exceptions:

👉 [Open a Structured GitHub Issue Ticket](https://github.com/Tony-Faijue/ODIRA-Object-Detection-Information-Recording-Application-/issues)
