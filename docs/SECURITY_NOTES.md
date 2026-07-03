# ITU AI CCTV - Security Notes

## Credentials

Never commit real CCTV usernames or passwords.

Do not commit:

- backend/.env
- .env
- Any screenshot showing CCTV credentials

Use backend/.env.example for placeholders only.

## CCTV User Account

Recommended:

Create a dedicated CCTV user for AI backend.

Example:

- Username: ai_backend
- Permission: Live view / RTSP only
- Avoid admin permission if possible

## Runtime Data

Runtime event logs and evidence images are ignored from Git.

Ignored paths:

- backend/data/events.jsonl
- backend/data/task-logs/
- backend/data/evidence/

## Face Recognition

Face recognition involves biometric data.

Before enabling identity recognition:

- Define clear purpose
- Get proper approval
- Notify affected users
- Limit who can access recognition results
- Set retention period
- Avoid storing unnecessary face data
- Keep audit logs

For early development, start with face detection only.

## Number Plate Recognition

Vehicle number plates may become personal data if linked to individuals or ownership records.

Recommended controls:

- Store only necessary events
- Limit access
- Define retention period
- Use for security purpose only
- Avoid public exposure

## Deployment

For production:

- Use an always-on Windows Server or dedicated monitoring PC
- Secure .env file
- Restrict folder permissions
- Keep GitHub repo free from secrets
- Backup only required evidence and logs
