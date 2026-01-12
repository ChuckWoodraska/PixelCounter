from app.config import settings


def test_read_main(client):
    response = client.get("/")
    assert response.status_code == 200
    assert "Pixel Metrics" in response.text

def test_upload_image(client):
    # Create a dummy image
    content = b"" # Needs to be valid image bytes for PIL
    # Let's create a minimal valid PNG
    import io

    from PIL import Image
    img = Image.new('RGB', (1, 1), color = 'red')
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    content = buf.getvalue()

    response = client.post(
        "/upload",
        files={"file": ("test.png", content, "image/png")}
    )
    assert response.status_code == 200
    assert "Results" in response.text
    assert "#ff0000" in response.text

def test_upload_too_large(client, monkeypatch):
    # Mock settings to have small limit
    monkeypatch.setattr(settings, "MAX_UPLOAD_SIZE_BYTES", 10)

    response = client.post(
        "/upload",
        files={"file": ("test.txt", b"a" * 20, "image/png")}
    )
    assert response.status_code == 413
    assert "File too large" in response.json()["detail"]

def test_upload_invalid_type(client):
    response = client.post(
        "/upload",
        files={"file": ("test.txt", b"abc", "text/plain")}
    )
    assert response.status_code == 400
    assert "Invalid file type" in response.json()["detail"]
