# Project Requirements

Dokumen ini menyenaraikan keperluan awal untuk projek **Hikvision AI CCTV Detection Project**.

## 1. Functional Requirements

### 1.1 CCTV Stream

Sistem perlu boleh:

- Sambung ke kamera/NVR Hikvision melalui RTSP.
- Menyokong lebih daripada satu kamera pada masa akan datang.
- Menggunakan main stream atau sub stream mengikut performance server.
- Reconnect secara automatik jika stream terputus.

### 1.2 AI Detection

Sistem perlu boleh mengesan sekurang-kurangnya:

- Person.
- Vehicle.
- Animal.
- Intrusion zone.
- Line crossing.

Detection lanjutan yang dicadangkan:

- PPE detection seperti helmet/vest/boot.
- Loitering detection.
- Crowd counting.
- Object left behind.

### 1.3 Event Logging

Apabila detection berlaku, sistem perlu:

- Simpan timestamp.
- Simpan nama kamera.
- Simpan jenis detection.
- Simpan confidence score.
- Simpan snapshot jika diperlukan.
- Simpan event dalam CSV, JSON, SQLite atau database lain.

### 1.4 Alert

Sistem perlu menyokong alert melalui sekurang-kurangnya satu channel:

- Telegram.
- Email.
- Dashboard local.

Alert perlu mengandungi:

- Masa event.
- Nama kamera.
- Jenis detection.
- Snapshot jika sesuai.

### 1.5 Dashboard

Dashboard minimum perlu memaparkan:

- Status kamera online/offline.
- Senarai event terkini.
- Snapshot event.
- Filter berdasarkan kamera dan jenis event.

## 2. Non-Functional Requirements

### 2.1 Security

- Credential tidak boleh hardcoded dalam source code.
- RTSP stream tidak boleh dibuka kepada public internet.
- Access dashboard perlu dikawal.

### 2.2 Performance

- Pilot awal hanya perlu support satu kamera.
- Sasaran awal: 5 hingga 15 FPS untuk detection, bergantung kepada hardware.
- Sub stream boleh digunakan untuk kurangkan beban CPU/GPU.

### 2.3 Reliability

- Sistem perlu reconnect jika stream timeout.
- Error perlu direkod dalam log.
- Sistem tidak patut crash hanya kerana satu kamera offline.

### 2.4 Maintainability

- Config kamera perlu berada dalam fail config, bukan hardcoded.
- Code perlu modular: stream, detection, alert, logging.
- Dokumentasi setup perlu jelas.

## 3. Pilot Scope

Pilot pertama:

- 1 kamera Hikvision.
- RTSP stream test berjaya dalam VLC.
- Detection person/vehicle.
- Snapshot event disimpan.
- Alert Telegram dihantar.
- Log event disimpan dalam CSV/JSON.

## 4. Out of Scope Untuk Fasa Awal

Perkara berikut tidak dibuat dahulu:

- Face recognition.
- Plate number recognition.
- Integrasi terus dengan sistem attendance.
- Cloud storage.
- Multi-branch monitoring.
- Full production dashboard.

## 5. Maklumat Yang Perlu Dikumpul

- Model NVR.
- Model kamera.
- Jumlah kamera.
- IP address NVR/kamera.
- RTSP port.
- Username read-only.
- Lokasi kamera.
- Use case detection untuk setiap kamera.
