# ITU AI CCTV - Live View

The dashboard live view is a backend MJPEG proxy for one selected camera at a time. It is for viewing only and does not run YOLO, save evidence, write event logs, send Telegram alerts, change event review, change identity assignment, change ignore zones, or affect the live monitor loop.

Assign Identity and multi-person targets come from saved event metadata, not from live-view pixels.

`/dashboard-tv` uses an iVMS-style single-camera live monitor layout. It keeps the camera dropdown/selection model and intentionally does not show a 13-camera simultaneous MJPEG grid.

## Endpoints

```text
GET /dashboard/live/{camera_id}/stream.mjpg?quality=standard
GET /dashboard/live/{camera_id}/stream.mjpg?quality=hd
GET /dashboard/live/{camera_id}/snapshot.jpg?quality=standard
GET /dashboard/live/{camera_id}/snapshot.jpg?quality=hd
```

Missing `quality` defaults to `standard`.

Invalid `quality` values return HTTP 400.

The TV dashboard defaults its selected live stream to HD and provides an HD / Standard toggle. Changing camera or quality restarts the MJPEG stream with a cache-busting query parameter and shows a reconnecting state.

## Quality Modes

- `standard`: uses the configured camera channel, usually Hikvision sub-stream `102`.
- `hd`: uses Hikvision channel `101`.

HD snapshot can preserve full source resolution where the camera provides it. A production test on `block_f_cam_7` confirmed an HD snapshot at 3200x1800. Actual resolution still depends on the camera main-stream settings and may be lower.

MJPEG live stream output is capped for browser performance. HD allows a larger max width than Standard, but it is still intended for one selected camera/viewer, not all cameras at once. Use Standard if HD is heavy for the TV, network, or camera.

## TV Controls

The TV live monitor includes:

- selected camera dropdown
- HD / Standard quality toggle
- camera name, camera ID, safe host metadata, selected quality, and live status
- restart stream button
- snapshot button using the selected quality
- fullscreen button when supported by the browser

## Audio

MJPEG has no audio. Some Hikvision cameras may have microphone/audio streams, but dashboard audio is not implemented.

Future audio requires a different media path such as HLS, WebRTC, or an FFmpeg-backed proxy.

## Security

Browsers never receive RTSP URLs, CCTV usernames, or CCTV passwords. The backend opens RTSP and serves MJPEG frames to the dashboard.
