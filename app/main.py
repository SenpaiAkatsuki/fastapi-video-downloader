from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from pathlib import Path
from yt_dlp import YoutubeDL
from imageio_ffmpeg import get_ffmpeg_exe
import tempfile, os

BASE_DIR = Path(__file__).parent
FFMPEG_BINARY = get_ffmpeg_exe()

app = FastAPI()

# 1) Mount static files under /static
app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")

# 2) Serve index.html at root
@app.get("/", include_in_schema=False)
async def index():
    return FileResponse(BASE_DIR / "static" / "index.html")


# Helper: get MP4‐only format info
def extract_info(url: str):
    ydl_opts = {
        "skip_download": True,
        "quiet": True,
        "no_warnings": True,
        "format": "bestvideo+bestaudio/best",
    }
    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)

    fmts = []
    for f in info.get("formats", []):
        if f.get("height") and f.get("vcodec") != "none" and f.get("ext") == "mp4":
            h = f["height"]
            fmts.append({
                "qualityLabel": f"{h}p",
                "quality": str(h),
                "container": f["ext"],
            })
    uniq = {x["quality"]: x for x in fmts}
    choices = sorted(uniq.values(), key=lambda x: int(x["quality"]), reverse=True)

    return {
        "title": info.get("title"),
        "thumbnailUrl": info.get("thumbnail"),
        "resolutions": choices,
    }


# 3) Info endpoint
@app.get("/api/info/")
async def api_info(url: str = Query(..., description="Video URL")):
    try:
        return JSONResponse(content=extract_info(url))
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Cannot extract info: {e}")


# 4) Download endpoint (exact height first, then fallback; H.264 + AAC)
@app.get("/api/download/")
async def api_download(
    url: str     = Query(..., description="Video URL"),
    quality: str = Query("1080", description="Height in px"),
    container: str = Query("mp4", description="Container"),
):
    tmpdir  = tempfile.mkdtemp()
    outtmpl = os.path.join(tmpdir, "%(title)s.%(ext)s")

    ydl_opts = {
        "format": (
            f"bestvideo[height={quality}][vcodec^=avc]+"
            f"bestaudio[ext=m4a]/"
            f"bestvideo[height<={quality}][vcodec^=avc]+"
            "bestaudio[ext=m4a]"
        ),
        "outtmpl": outtmpl,
        "merge_output_format": container,
        "ffmpeg_location":     FFMPEG_BINARY,
        "quiet": True,
    }

    try:
        with YoutubeDL(ydl_opts) as ydl:
            ydl.extract_info(url, download=True)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Download error: {e}")

    files = os.listdir(tmpdir)
    if not files:
        raise HTTPException(status_code=500, detail="No file found")

    return FileResponse(
        path=os.path.join(tmpdir, files[0]),
        filename=files[0],
        media_type=f"video/{container}"
    )
