import json
import re
from pathlib import Path
from markdown import markdown
from glob import glob

Path("json").mkdir(exist_ok=True)
Path("html").mkdir(exist_ok=True)

def remove_private_use_chars(text):
    return re.sub(r'[\uE000-\uF8FF]', '', text)

with open("conversations.json", "r", encoding="utf-8") as f:
    conversations = json.load(f)

generated_html_files = []

for i, convo in enumerate(conversations):
    title = convo.get("title", f"chat_{i}")
    safe_title = re.sub(r"[\W]+", "_", title.strip())
    json_path = Path("json") / f"{safe_title}.json"
    html_path = Path("html") / f"{i+1}_{safe_title}.html"
    generated_html_files.append((f"{i+1}. {title}", html_path.name))

    with open(json_path, "w", encoding="utf-8") as out:
        json.dump(convo, out, indent=2)

    mapping = convo["mapping"]

    def extract_message_html(msg):
        role = msg["author"]["role"]
        content = msg.get("content", {})
        parts = content.get("parts", [])
        bubble_class = "user" if role == "user" else "assistant"
        output = ""

        for part in parts:
            if isinstance(part, str) and part.strip():
                lines = [remove_private_use_chars(line) for line in part.split("\n")]
                converted = []
                for line in lines:
                    if re.match(r'^https?:\/\/.*\.(png|jpg|jpeg|gif)$', line.strip(), re.IGNORECASE):
                        line = f"![image]({line.strip()})"
                    converted.append(line)
                rendered = markdown("\n".join(converted), extensions=["fenced_code"])
            elif isinstance(part, dict) and part.get("content_type") == "image_asset_pointer":
                asset_id = part.get("asset_pointer", "").replace("file-service://", "")
                matches = glob(f"{asset_id}*")
                if matches:
                    filename = Path(matches[0]).name
                    rendered = f'<div class="image-frame"><img src="../{filename}" alt="image"></div>'
                else:
                    rendered = f'<div class="image-frame"><div style="color:gray;">[Image {asset_id} not found]</div></div>'
            else:
                continue

            output += f"<div class='bubble {bubble_class}'><div class='content'>{rendered}</div></div>\n"

        return output

    def traverse_html(node_id):
        node = mapping[node_id]
        msg = node.get("message")
        html = ""
        if msg:
            html += extract_message_html(msg)
        for child_id in node.get("children", []):
            html += traverse_html(child_id)
        return html

    root_id = next(k for k, v in mapping.items() if v["parent"] is None)
    conversation_html = traverse_html(root_id)

    html_output = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>{title}</title>
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, Segoe UI, Roboto, Helvetica, Arial, sans-serif;
            background: #e5ddd5;
            margin: 0;
            padding: 20px;
        }}
        .chat-container {{
            max-width: 1200px;
            margin: 0 auto;
        }}
        .bubble {{
            max-width: 85%;
            padding: 12px 16px;
            margin: 10px;
            border-radius: 16px;
            line-height: 1.5;
            word-wrap: break-word;
            box-shadow: 0 1px 2px rgba(0, 0, 0, 0.15);
        }}
        .user {{
            background-color: #dcf8c6;
            margin-left: auto;
        }}
        .assistant {{
            background-color: #ffffff;
            margin-right: auto;
        }}
        .content pre {{
            background-color: #f0f0f0;
            padding: 10px;
            border-radius: 8px;
            overflow-x: auto;
            white-space: pre-wrap;
            word-break: break-word;
            margin-top: 10px;
        }}
        .content code {{
            background-color: #eee;
            padding: 2px 4px;
            border-radius: 4px;
            font-family: monospace;
        }}
        .content h1, .content h2, .content h3, .content h4 {{
            font-size: 16px;
            margin: 8px 0;
            text-align: left;
        }}
        .content img {{
            max-width: 100%;
            height: auto;
            border-radius: 8px;
            margin-top: 10px;
            cursor: pointer;
        }}
        .image-frame img {{
            max-width: 100%;
            border-radius: 12px;
            border: 1px solid #ccc;
            margin-top: 10px;
            cursor: pointer;
        }}
        .fullscreen-overlay {{
            position: fixed;
            top: 0; left: 0;
            width: 100%; height: 100%;
            background: rgba(0,0,0,0.9);
            display: none;
            align-items: center;
            justify-content: center;
            z-index: 9999;
        }}
        .fullscreen-overlay img {{
            max-width: 95%;
            max-height: 95%;
            border-radius: 10px;
        }}
    </style>
</head>
<body>
<div class="chat-container" dir="auto" style="unicode-bidi: plaintext;">
<h2>{title}</h2>
<p><a href="../index.html">← Back to Home</a></p>
{conversation_html}
<p><a href="../index.html">← Back to Home</a></p>
</div>
<div class="fullscreen-overlay" id="imgOverlay" onclick="this.style.display='none'">
  <img id="overlayImg" src="" alt="fullscreen">
</div>
<script>
  document.querySelectorAll("img").forEach(img => {{
    img.onclick = function () {{
      document.getElementById("overlayImg").src = this.src;
      document.getElementById("imgOverlay").style.display = "flex";
    }};
  }});
</script>
</body>
</html>
"""
    Path(html_path).write_text(html_output, encoding="utf-8")
    print(f"Saved HTML: {html_path}")

index_html = """<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>ChatGPT Backup Index</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background: #f4f4f4;
            padding: 40px;
        }
        h1 {
            text-align: center;
            color: #333;
        }
        ul {
            max-width: 600px;
            margin: 20px auto;
            padding: 0;
            list-style-type: none;
        }
        li {
            background: #fff;
            margin: 10px 0;
            padding: 15px 20px;
            border-radius: 8px;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        }
        a {
            text-decoration: none;
            color: #007acc;
            font-weight: bold;
        }
        a:hover {
            text-decoration: underline;
        }
    </style>
</head>
<body>
    <h1>ChatGPT Conversations</h1>
    <ul>
"""

for name, filename in generated_html_files:
    index_html += f'        <li><a href="html/{filename}">{name.replace("_", " ")}</a></li>\n'

index_html += """    </ul>
</body>
</html>
"""

Path("index.html").write_text(index_html, encoding="utf-8")
print("Saved index.html")
