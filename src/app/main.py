from fastapi import FastAPI, File, HTTPException, Request, UploadFile
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from app.config import settings
from app.utils import process_image

app = FastAPI(title="Pixel Metrics App")

templates = Jinja2Templates(directory="src/app/templates")

@app.get("/", response_class=HTMLResponse)
async def index(request: Request) -> HTMLResponse:
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/upload", response_class=HTMLResponse)
async def upload_file(request: Request, file: UploadFile = File(...)) -> HTMLResponse:
    # Validate file size
    # FastAPI/Starlette doesn't easily expose content-length for validation before read,
    # but we can check if it's too large while reading or rely on a proxy.
    # For this task, we will read and check size.

    # Note: For strict 100MB limit, reading into memory might fail if server has low RAM,
    # but requirement says "process in memory" and "max upload 100MB", so we assume server can handle it.

    content = await file.read()

    if len(content) > settings.MAX_UPLOAD_SIZE_BYTES:
        raise HTTPException(status_code=413, detail="File too large")

    if file.content_type is None or not file.content_type.startswith("image/"):
        raise HTTPException(
            status_code=400, detail="Invalid file type. Please upload an image."
        )

    try:
        metrics = process_image(content)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing image: {str(e)}")

    return templates.TemplateResponse("results.html", {"request": request, "metrics": metrics})
