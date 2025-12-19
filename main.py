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
        "format": "best"
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)

            video_url = info.get("url")
            if not video_url and "formats" in info:
                video_url = info["formats"][-1]["url"]

        if not video_url:
            return jsonify({"error": "Unable to extract video"})

        return redirect(video_url)

    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == "__main__":
    app.run()
