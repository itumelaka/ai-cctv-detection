# System Architecture

Dokumen ini menerangkan architecture awal untuk projek **Hikvision AI CCTV Detection Project**.

## Overview

Sistem akan mengambil live stream daripada CCTV Hikvision, menjalankan AI detection pada frame video, kemudian menghasilkan event, snapshot dan alert apabila syarat detection dipenuhi.

## High Level Flow

```text
[Hikvision Camera/NVR]
          |
          | RTSP / ONVIF
          v
[Stream Reader]
          |
          | Video Frames
          v
[AI Detection Engine]
          |
          | Detection Result
          v
[Event Processor]
          |
          +--> [Snapshot Storage]
          +--> [Event Log / Database]
          +--> [Alert Service]
          +--> [Dashboard]
```

## Main Components

### 1. Hikvision Camera/NVR

Sumber video utama. Sistem akan menggunakan RTSP stream daripada kamera atau NVR.

Contoh stream:

```text
rtsp://username:password@IP_ADDRESS:554/Streaming/channels/101
```

### 2. Stream Reader

Tugas:

- Buka RTSP stream.
- Ambil frame video.
- Reconnect jika stream gagal.
- Pilih main stream atau sub stream.

Cadangan library:

- OpenCV.
- FFmpeg.
- GStreamer.

### 3. AI Detection Engine

Tugas:

- Terima frame daripada stream reader.
- Jalankan object detection.
- Pulangkan object class, confidence dan bounding box.

Cadangan engine:

- YOLO / Ultralytics.
- Frigate.
- OpenVINO.
- TensorRT untuk NVIDIA hardware.

### 4. Event Processor

Tugas:

- Tentukan sama ada detection perlu dijadikan event.
- Kurangkan duplicate alert menggunakan cooldown.
- Semak zone/line crossing jika digunakan.
- Simpan metadata event.

Contoh event:

```json
{
  "timestamp": "2026-07-02T23:00:00+08:00",
  "camera_id": "CAM01",
  "camera_name": "Pintu Masuk Utama",
  "event_type": "person_detected",
  "confidence": 0.87,
  "snapshot": "events/CAM01_20260702_230000.jpg"
}
```

### 5. Alert Service

Tugas:

- Hantar alert kepada PIC.
- Sertakan maklumat event.
- Sertakan snapshot jika perlu.

Channel cadangan:

- Telegram.
- Email.
- Dashboard notification.

### 6. Storage

Jenis storage awal:

- Folder local untuk snapshot.
- CSV/JSON untuk log awal.
- SQLite jika mahu lebih tersusun.

Production option:

- PostgreSQL.
- Network storage.
- Object storage dalaman.

### 7. Dashboard

Dashboard awal boleh jadi simple:

- HTML page local.
- Flask/FastAPI web app.
- Node.js dashboard.
- Grafana jika guna database/time-series.

## Deployment Option

### Option A: Mini PC Local

Sesuai untuk pilot kecil.

```text
Hikvision NVR → Mini PC → AI Detection → Telegram/Dashboard
```

Kelebihan:

- Murah.
- Senang deploy.
- Sesuai untuk 1-4 kamera bergantung spec.

### Option B: NVIDIA Jetson

Sesuai untuk edge AI.

```text
Hikvision NVR → NVIDIA Jetson → TensorRT AI Detection → Alert
```

Kelebihan:

- Power efficient.
- Sesuai untuk AI video.
- Boleh jalan local tanpa cloud.

### Option C: Server GPU

Sesuai untuk banyak kamera.

```text
Hikvision NVR → GPU Server → Multi-Camera AI Detection → Dashboard
```

Kelebihan:

- Performance tinggi.
- Senang scale.
- Sesuai untuk production.

## Security Architecture

```text
CCTV LAN/VLAN
      ↓ restricted access
AI Server
      ↓ authenticated access
Dashboard / Alert
```

Rule penting:

- Jangan expose RTSP ke internet.
- Gunakan read-only user.
- Simpan credential dalam `.env`.
- Limit access dashboard.
