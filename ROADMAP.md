# Project Roadmap

Roadmap ini disusun untuk membangunkan projek **Hikvision AI CCTV Detection Project** secara berperingkat.

## Phase 0: Documentation and Planning

Status: In Progress

Tasks:

- Sediakan README.md.
- Sediakan SECURITY.md.
- Sediakan REQUIREMENTS.md.
- Sediakan ARCHITECTURE.md.
- Senaraikan kamera/NVR yang terlibat.
- Tetapkan use case pilot.

Deliverable:

- Dokumentasi asas projek lengkap.

## Phase 1: RTSP Pilot Test

Tasks:

- Dapatkan IP NVR/kamera.
- Cipta user read-only untuk stream.
- Test RTSP dalam VLC.
- Test main stream dan sub stream.
- Rekod format RTSP yang berjaya.

Acceptance Criteria:

- Satu kamera berjaya live view melalui RTSP.
- Stream stabil sekurang-kurangnya 30 minit.

## Phase 2: Basic AI Detection Prototype

Tasks:

- Setup Python environment.
- Install OpenCV dan YOLO/Ultralytics.
- Baca RTSP stream.
- Detect person/vehicle.
- Papar bounding box pada preview window.

Acceptance Criteria:

- Sistem boleh detect person/vehicle daripada live CCTV.
- FPS dan CPU/GPU usage direkod.

## Phase 3: Event Logging and Snapshot

Tasks:

- Simpan snapshot apabila detection berlaku.
- Simpan event log dalam CSV/JSON.
- Tambah cooldown untuk elak spam event.
- Tambah camera name dan timestamp.

Acceptance Criteria:

- Event detection menghasilkan snapshot dan log.
- Duplicate alert terkawal.

## Phase 4: Alert System

Tasks:

- Setup Telegram Bot atau email alert.
- Hantar alert apabila event berlaku.
- Sertakan snapshot jika sesuai.
- Tambah setting enable/disable alert per kamera.

Acceptance Criteria:

- PIC menerima alert dengan maklumat event.
- Alert tidak spam berulang tanpa kawalan.

## Phase 5: Dashboard Basic

Tasks:

- Papar status kamera.
- Papar senarai event terkini.
- Papar snapshot event.
- Tambah filter kamera/event type.

Acceptance Criteria:

- Dashboard boleh dibuka dalam LAN.
- Event terkini boleh disemak oleh PIC.

## Phase 6: Advanced Detection

Possible features:

- Intrusion zone.
- Line crossing.
- PPE detection.
- Animal detection.
- After-hours detection.
- Crowd counting.
- Loitering detection.

Acceptance Criteria:

- Use case lanjutan diuji satu per satu.
- False positive direkod dan dikurangkan.

## Phase 7: Production Hardening

Tasks:

- Service auto-start.
- Log rotation.
- Config backup.
- Access control dashboard.
- Monitoring CPU/GPU/storage.
- Retention policy snapshot/log.

Acceptance Criteria:

- Sistem boleh berjalan stabil untuk tempoh panjang.
- Ada SOP restart, backup dan troubleshooting.

## Suggested First Pilot

Cadangan paling selamat:

```text
Kamera: Pintu masuk / laluan umum
Detection: Person detected after office hours
Alert: Telegram
Storage: Snapshot + CSV log
```

Sebab:

- Use case jelas.
- Risiko privacy lebih rendah berbanding kawasan sensitif.
- Mudah validate sama ada detection tepat atau tidak.
