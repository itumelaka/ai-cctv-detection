# ITU AI CCTV - Live View

The dashboard live view is for one selected camera at a time. `/dashboard-tv` defaults to MediaMTX WebRTC Smooth mode for display and keeps the backend MJPEG proxy as fallback. It is for viewing only and does not run YOLO, save evidence, write event logs, send Telegram alerts, change event review, change identity assignment, change ignore zones, or affect the live monitor loop.

Assign Identity and multi-person targets come from saved event metadata, not from live-view pixels.

`/dashboard-tv` uses an iVMS-style single-camera live monitor layout. It keeps the camera dropdown/selection model and intentionally does not show a 13-camera simultaneous grid.

## Endpoints

```text
GET /dashboard/live/{camera_id}/stream.mjpg?quality=standard
GET /dashboard/live/{camera_id}/stream.mjpg?quality=hd
GET /dashboard/live/{camera_id}/snapshot.jpg?quality=standard
GET /dashboard/live/{camera_id}/snapshot.jpg?quality=hd
```

Missing `quality` defaults to `standard`.

Invalid `quality` values return HTTP 400.

The TV dashboard defaults its selected live stream to WebRTC Smooth. It also provides MJPEG Fallback with a Smooth Live / HD Live toggle. Changing camera, live mode, or fallback quality restarts the selected stream with a cache-busting query parameter or refreshed viewer URL and shows a reconnecting state.

## WebRTC Smooth Mode

The TV dashboard defaults to WebRTC Smooth mode through a local MediaMTX gateway on port `8889`. The browser URL is built from the current dashboard hostname:

```text
http://<dashboard-host>:8889/{camera_id}/
```

The MediaMTX path name should match the dashboard `camera_id`. RTSP source URLs and camera credentials remain server-side and are not exposed to the browser. If a selected camera path is not configured in MediaMTX yet, use MJPEG Fallback.

WebRTC quality is controlled by the MediaMTX/camera path for now. The Smooth Live / HD Live quality toggle applies only to MJPEG Fallback mode.

## Quality Modes

- `standard`: used by MJPEG Fallback Smooth Live. It uses the configured camera channel, usually Hikvision sub-stream `102`.
- `hd`: used by MJPEG Fallback HD Live and HD snapshots. It uses Hikvision channel `101`.

HD snapshot can preserve full source resolution where the camera provides it. A production test on `block_f_cam_7` confirmed an HD snapshot at 3200x1800. Actual resolution still depends on the camera main-stream settings and may be lower.

MJPEG live stream output is capped for browser performance. WebRTC Smooth is the default display path. MJPEG HD Live remains available for detail viewing, but can be heavier for the TV, network, or camera. HD snapshots and evidence crops use the HD evidence/snapshot paths separately from the live display mode.

## TV Controls

The TV live monitor includes:

- selected camera dropdown
- WebRTC Smooth / MJPEG Fallback live mode toggle
- Smooth Live / HD Live quality toggle for MJPEG Fallback
- camera name, camera ID, safe host metadata, selected live mode, and live status
- restart stream button
- snapshot button that defaults to HD even when live display is Smooth
- fullscreen button when supported by the browser

## Audio

Dashboard audio is not implemented. Some Hikvision cameras may have microphone/audio streams, but this pass keeps live view video-only.

Future audio requires camera audio support plus a suitable media path.

## Security

Browsers never receive RTSP URLs, CCTV usernames, or CCTV passwords. MediaMTX and the backend handle camera sources server-side; the dashboard only receives WebRTC viewer pages or backend MJPEG/snapshot output.
