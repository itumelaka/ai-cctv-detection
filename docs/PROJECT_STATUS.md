# ITU AI CCTV - Project Status

Last updated: 2026-07-03

## Current Project Goal

Build an internal AI CCTV backend system using existing Hikvision CCTV infrastructure at ITU Melaka.

The long-term target is to create a self-managed AI CCTV system with:

- Multi-camera CCTV monitoring
- Person detection
- Event logging
- Evidence snapshot storage
- Face detection and recognition
- Vehicle and number plate recognition
- Dashboard and alerting system

## Current Working Foundation

The backend is currently running on FastAPI and has been tested locally using a Hikvision CCTV RTSP stream.

## Confirmed Working Camera

| Camera ID | Name | IP Address | Channel | Status |
|---|---|---:|---:|---|
| block_f_cam_9 | ITU BLOCK F CAM9 | 192.168.40.21 | 102 | Confirmed working |
| block_e_cam_2 | ITU BLOCK E CAM2 | 192.168.40.14 | 102 | Person detection confirmed |

## Camera Stream Configuration

Recommended CCTV stream for AI processing:

| Setting | Value |
|---|---|
| Stream Type | Sub-stream |
| Codec | H.264 |
| Resolution | 640x360 |
| RTSP Channel | 102 |
| Bitrate | Around 512 Kbps |

Avoid H.265 / HEVC for backend AI processing because OpenCV may timeout or fail to decode the stream reliably on Windows.

## Working Backend Features

### Camera

- GET /cameras/list
- GET /cameras/enabled
- GET /cameras/test
- GET /cameras/snapshot
- GET /cameras/{camera_id}/test

### Detection

- GET /detections/test
- GET /detections/yolo
- GET /detections/yolo/snapshot
- GET /detections/person
- GET /detections/person/snapshot
- GET /detections/{camera_id}/person
- GET /detections/{camera_id}/person/snapshot

### Events

- GET /events/person
- GET /events/logs
- GET /events/stats
- GET /events/evidence/{filename}

### Monitor

- GET /monitor/person/check
- GET /monitor/{camera_id}/person/check

## Local Scheduler Status

Windows Task Scheduler pilot has been created:

Task name:

ITU AI CCTV Person Monitor

Current behaviour:

- Runs person monitor check automatically
- Writes output to backend/data/task-logs/monitor_person.log
- Uses hidden VBS launcher to avoid CMD popup
- Currently should remain disabled while multi-camera development continues

## Runtime Data

Runtime files are not committed to GitHub.

Ignored runtime paths:

- backend/data/events.jsonl
- backend/data/task-logs/
- backend/data/evidence/
- *.pt YOLO model weights

## Current Development Focus

The project is currently moving from single-camera monitoring to multi-camera monitoring.

Next technical focus:

1. Camera audit endpoint
2. Monitor all enabled cameras
3. Multi-camera scheduler script
4. Evidence snapshot per camera
5. Dashboard-ready API response
