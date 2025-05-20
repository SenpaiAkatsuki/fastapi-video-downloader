# FastAPI Video Downloader

A simple video downloader service built with FastAPI, allowing user to fetch and download YouTube, TikTok, Instagram and other supported videos as H.264 + AAC MP4 at the exact resolution they choose

---

## Key Features

- **Exact‐Resolution MP4**: True H.264 video + AAC audio in MP4 container at 144p–1080p+  
- **Zero‐Config FFmpeg**: Bundled automatically via `imageio-ffmpeg`  
- **Unified App**: Serves both UI and API from one FastAPI application  
- **Wide Platform Support**: Leverages `yt-dlp` to handle YouTube, Shorts, TikTok, Instagram, and more  
- **No Build Steps**: Static assets served directly—just clone and run  

---

## Technologies

- **Python 3.8+**  
- **FastAPI** & **Uvicorn**  
- **yt-dlp** & **imageio-ffmpeg**  
- **HTML5**, **CSS3**, **Vanilla JavaScript**  


## First Setup

1. **Upgrade pip & install dependencies**  
   pip install --upgrade pip
   pip install -r requirements.txt

2. **Confirm FFmpeg bundle**
   python -c "from imageio_ffmpeg import get_ffmpeg_exe; print(get_ffmpeg_exe())"

3. **Launch the App**
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

4. **Use the UI**
   Open your browser at http://localhost:8000/


