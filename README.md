# Hikvision AI CCTV Detection Project

Projek ini bertujuan membina sistem **AI CCTV Detection** menggunakan kamera/NVR Hikvision sedia ada di institut. Sistem ini akan mengambil video stream daripada CCTV melalui RTSP/ONVIF, memproses video menggunakan model AI detection, dan menghasilkan alert/event log apabila objek atau situasi tertentu dikesan.

## Objektif Projek

1. Menggunakan infrastruktur CCTV Hikvision sedia ada tanpa perlu menukar semua kamera.
2. Menambah fungsi AI detection seperti manusia, kenderaan, haiwan, PPE, intrusion, line crossing dan aktiviti mencurigakan.
3. Menyediakan sistem alert untuk notifikasi kepada PIC melalui Telegram, email atau dashboard dalaman.
4. Menyimpan snapshot dan log event sebagai rujukan keselamatan.
5. Melaksanakan projek secara berperingkat bermula dengan pilot satu kamera dahulu.

## Skop Awal

Fasa awal projek akan fokus kepada:

- Sambungan ke satu kamera/NVR Hikvision melalui RTSP.
- Ujian live stream menggunakan VLC atau FFmpeg.
- AI detection asas menggunakan YOLO/OpenCV/Frigate.
- Detection manusia dan kenderaan.
- Simpan snapshot apabila detection berlaku.
- Paparan log ringkas melalui dashboard atau folder event.
- Alert asas melalui Telegram atau email.

## Cadangan Architecture

```text
Hikvision CCTV / NVR
        ↓ RTSP / ONVIF
Mini PC / Server / NVIDIA Jetson
        ↓
AI Detection Engine
        ↓
Event Processor
        ↓
Alert + Snapshot + Dashboard + Log
```

## Contoh Use Case

- Kesan orang masuk kawasan larangan.
- Kesan pergerakan selepas waktu pejabat.
- Kira jumlah orang dalam kawasan tertentu.
- Kesan kenderaan masuk/keluar.
- Kesan haiwan masuk kawasan kandang/lab.
- Kesan pemakaian PPE seperti helmet, vest atau kasut keselamatan.
- Simpan snapshot apabila event berlaku.
- Hantar alert kepada pegawai bertanggungjawab.

## Keperluan Minimum

### Hardware

- Hikvision IP Camera atau NVR yang support RTSP/ONVIF.
- Mini PC / server / workstation.
- Network LAN yang stabil.
- Storage untuk snapshot dan log.
- Optional: NVIDIA GPU, NVIDIA Jetson, Google Coral TPU.

### Software

- Windows atau Linux.
- Python 3.10+.
- OpenCV.
- YOLO / Ultralytics atau Frigate.
- FFmpeg atau VLC untuk test stream.
- Telegram Bot API atau SMTP untuk alert.

## Contoh RTSP Hikvision

```text
rtsp://username:password@IP_ADDRESS:554/Streaming/channels/101
```

Contoh channel:

```text
101 = Channel 1 main stream
102 = Channel 1 sub stream
201 = Channel 2 main stream
202 = Channel 2 sub stream
```

> Nota: Jangan expose RTSP stream ke internet. Gunakan LAN/VPN sahaja.

## Status Projek

Status semasa: **Planning / Documentation Stage**

Belum ada production deployment. Projek akan dimulakan dengan pilot satu kamera terlebih dahulu.

## Struktur Cadangan Repo

```text
hikvision-ai-cctv/
├── README.md
├── SECURITY.md
├── REQUIREMENTS.md
├── ARCHITECTURE.md
├── ROADMAP.md
├── docs/
│   ├── rtsp-test.md
│   ├── camera-inventory.md
│   └── detection-use-cases.md
├── src/
│   ├── main.py
│   ├── config.py
│   ├── detector.py
│   ├── stream.py
│   └── alerts.py
├── config/
│   └── cameras.example.json
├── events/
│   └── .gitkeep
└── requirements.txt
```

## Prinsip Pelaksanaan

- Mula kecil dengan satu kamera dahulu.
- Gunakan user read-only untuk akses CCTV stream.
- Jangan simpan password sebenar dalam GitHub.
- Semua credential perlu disimpan dalam `.env` atau config tempatan yang tidak di-commit.
- Utamakan penggunaan LAN/VPN, bukan public internet.
- Pastikan penggunaan CCTV mematuhi polisi organisasi dan privasi.

## Next Step

1. Senaraikan model NVR dan kamera Hikvision.
2. Kenal pasti IP NVR/kamera.
3. Test RTSP satu kamera menggunakan VLC.
4. Pilih detection use case pertama.
5. Bina prototype AI detection.
6. Tambah alert dan event log.
7. Review performance sebelum tambah kamera lain.
