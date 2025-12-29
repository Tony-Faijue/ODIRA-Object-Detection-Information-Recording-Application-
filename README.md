
# ODIRA (Object Detection Recording Application)

This is a web application made with Angular framework, TypeScript, NGX-Webcam library, Python, OpenCV library, MobileNet SSD v3 model and FastAPI. Users can upload an image or take a picture using their webcam to detect for specified objects within the image. When a successful detection occurs users receive the resulting image with confidence percentages and boundary boxes drawn around the objects, as well as a table that displays the class of objects detected, count per classs and total count of objects detected.

## Goal
The purpose of this application is to allow users to detect objects within images by identifying the class and counting the amount of objects detected. Users have control over the Object Detection Threshold & NMS Threshold parameters and selecting which category of objects to detect allowing for stricter or looser filtering for their object detection needs. 

## What I Learned
This project has taught me more about Computer Vision such as working with the OpenCV library, loading and configuring a pretrained object detection model and utlizing the FASTAPI library to create API endpoints, and handling sending and responding to request from the client. I was able to apply things that I have learned to better improve the interface for the users such as tooltips, sliders for range of values, and error message to provide informative feedback.

## Tech Stack
**Client:** Angular, TypeScript, HTML/CSS, TailwindCSS, NGX-Webcam

**Server:** FastAPI, Python, OpenCV

## Configurations
- Git
### Python
- Python = 3.13
- pip = 23.2.1
- opencv-python = 4.12.0.88

### Angular/TypeScript
- TypeScript = 5.8.3
- angular/cli = 20.3.10
- Node.JS = 24.6.0

## Installations and Running Locally

Install PyCharm IDE
https://www.jetbrains.com/pycharm/

Install NodeJS
https://nodejs.org/en

### 2. Follow Docs to Install PyCharm IDE and NodeJS
Install NodeJS
```bash
  npm install
```
### Import & Install Python Libraries
- opencv-python
- pydantic
- starlette
- apscheduler

```bash
  pip install fastapi
```

## Quickstart
### 1. Clone the repository
```bash
  git clone https://github.com/Tony-Faijue/ODIRA-Object-Detection-Information-Recording-Application-
```
### 2. For Angular Client run cmd:
```bash
  ng serve
```
### 3. For Python/FastAPI Server run cmd:
```bash
fastapi dev odiraserver.py --port 9998
```
## Report any Issues
There is bound to be issues within the application.
If you find something wrong, Open a GitHub Issue:

👉 [Report a bug on GitHub](https://github.com/Tony-Faijue/ODIRA-Object-Detection-Information-Recording-Application-/issues)

