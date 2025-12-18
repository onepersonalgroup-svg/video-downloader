from flask import Flask, request, jsonify
import yt_dlp

app = Flask(__name__)

@app.route("/")
def home():
    return "Video Downloader API Running"

@app.route("/meta")
def meta():
    url = request.args.get("url")
    if not url:
        return jsonify({"error": "No URL provided"})

    ydl_opts = {
        "quiet": True,
        "skip_download": True,
        "format": "best"
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)

            video_url = info.get("url")
            if not video_url and "formats" in info:
                for f in reversed(info["formats"]):
                    if f.get("url"):
                        video_url = f["url"]
                        break

        if not video_url:
            return jsonify({"error": "No video found"})

        return jsonify({
            "title": info.get("title"),
            "thumbnail": info.get("thumbnail"),
            "video_url": video_url
        })

    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == "__main__":
    app.run()
