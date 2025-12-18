from flask import Flask, request, redirect, jsonify
import yt_dlp

app = Flask(__name__)

@app.route("/")
def home():
    return "Video Downloader API Running"

@app.route("/download")
def download():
    url = request.args.get("url")
    if not url:
        return jsonify({"error": "No URL provided"})

    ydl_opts = {
        "quiet": True,
        "skip_download": True,
        "format": "best",
        "nocheckcertificate": True,
        "extractor_args": {
            "facebook": {
                "include_dash_manifest": False
            }
        },
        "user_agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/120.0 Safari/537.36"
        ),
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)

            if not info:
                return jsonify({"error": "Extraction failed"})

            # Prefer direct URL
            video_url = info.get("url")

            # Fallback to formats
            if not video_url and "formats" in info:
                for f in reversed(info["formats"]):
                    if f.get("url"):
                        video_url = f["url"]
                        break

            if not video_url:
                return jsonify({"error": "No video URL found"})

            return redirect(video_url)

    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == "__main__":
    app.run()
