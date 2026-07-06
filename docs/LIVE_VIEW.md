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

The TV dashboard defaults its selected live stream to Smooth Live, which uses the existing Standard endpoint for better TV performance. It provides a Smooth Live / HD Live toggle. Changing camera or quality restarts the MJPEG stream with a cache-busting query parameter and shows a reconnecting state.

## Quality Modes

- `standard`: used by Smooth Live. It uses the configured camera channel, usually Hikvision sub-stream `102`.
- `hd`: used by HD Live and HD snapshots. It uses Hikvision channel `101`.

HD snapshot can preserve full source resolution where the camera provides it. A production test on `block_f_cam_7` confirmed an HD snapshot at 3200x1800. Actual resolution still depends on the camera main-stream settings and may be lower.

MJPEG live stream output is capped for browser performance. Smooth Live is optimized for display. HD Live remains available for detail viewing, but can be heavier for the TV, network, or camera. HD snapshots and evidence crops use the HD evidence/snapshot paths separately from the smooth live display.

## TV Controls

The TV live monitor includes:

- selected camera dropdown
- Smooth Live / HD Live quality toggle
- camera name, camera ID, safe host metadata, selected quality, and live status
- restart stream button
- snapshot button that defaults to HD even when live display is Smooth
- fullscreen button when supported by the browser

## Audio

MJPEG has no audio. Some Hikvision cameras may have microphone/audio streams, but dashboard audio is not implemented.

Future audio requires a different media path such as HLS, WebRTC, or an FFmpeg-backed proxy.

## Security

Browsers never receive RTSP URLs, CCTV usernames, or CCTV passwords. The backend opens RTSP and serves MJPEG frames to the dashboard.
