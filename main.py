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
        video_url = info.get("url")

    return redirect(video_url)

if __name__ == "__main__":
    app.run()