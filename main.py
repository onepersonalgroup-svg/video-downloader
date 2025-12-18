from flask import Flask, request, jsonify, redirect
import yt_dlp

app = Flask(__name__)

@app.route("/")
def home():
    return "Direct Video Link API Running"

@app.route("/download")
def download():
    url = request.args.get("url")
    if not url:
        return jsonify({"error": "No URL provided"})

    ydl_opts = {
        "quiet": True,
        "skip_download": True
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)

        video_url = None

        # ✅ FIX: get best video URL from formats
        if "formats" in info and info["formats"]:
            video_url = info["formats"][-1]["url"]
        elif "url" in info:
            video_url = info["url"]

    if not video_url:
        return jsonify({"error": "Unable to extract video link"})

    return redirect(video_url)

if __name__ == "__main__":
    app.run()
