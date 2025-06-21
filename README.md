# ChatGPT Backup Viewer

A simple offline viewer for your exported ChatGPT conversations. This script converts your `conversations.json` file into clean, readable HTML pages with clickable navigation and local image support.

---

## Features

- Converts all ChatGPT conversations to individual HTML files
- Automatically extracts and displays local images if available
- Creates an index homepage to navigate between chats
- Adds "Back to Home" links in each conversation
- Basic readable design for chat bubbles and code blocks
- Fully offline. No internet required.

---

## How to Use (Simple Version - For Non-Developers)

1. Download and unzip the latest `.zip` release.
2. Place your `conversations.json` file next to `main.exe`.
3. Double-click `main.exe`.
4. A new folder named `html` will be created. Open `index.html` to view your chats.

---

## How to Export Your ChatGPT Backup

1. Go to [https://chat.openai.com](https://chat.openai.com).
2. Click on your name (bottom-left) → **Settings**.
3. Go to **Data Controls** → **Export Data**.
4. Click **Export**, wait for the email, and download the `.zip` file.
5. Extract it and find `conversations.json`. Use this file with the app.

---

## Developer Instructions

1. Install dependencies:

```bash
pip install markdown
```

2. Run manually:

```bash
python main.py
```

---

## SHA256 Checksum (For .exe Verification)

```
c0ca90cb0ea5b6da23364342af06105592500b2a60e5459b95515fbf5f0606b3
```

To verify:

```bash
certutil -hashfile main.exe SHA256
```

---

## Notes

- The script is standalone. No server or Python setup needed for `.exe` users.
- For Linux/macOS users: use `python main.py` after installing Python and dependencies.
- Export your data from https://chat.openai.com/export

---

## License

MIT
