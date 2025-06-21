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

## Download

[Download main.exe](https://github.com/kirilldevs/chatgpt-backup-format/releases/download/v1.0.0/main.exe)

SHA-256: `f23b7eb9e340f011d3bb03e1413d73aec0e62a47b66a67e98ffa9e86a5e0e164`

To verify:

```bash
certutil -hashfile main.exe SHA256
```

---

## How to Use (Simple Version - For Non-Developers)

1. Download and unzip the latest `.zip` release.  
2. Place your `conversations.json` file next to `main.exe`.  
3. Double-click `main.exe`.  
4. A new folder named `html` will be created. Open `index.html` to view your chats.

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

## Notes

- The script is standalone. No server or Python setup needed for `.exe` users.  
- For Linux/macOS users: use `python main.py` after installing Python and dependencies.  
- Export your data from https://chat.openai.com/export

---

## License

MIT
