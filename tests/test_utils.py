import io

import numpy as np
from PIL import Image

from app.utils import process_image


def test_process_image_simple():
    # Create a simple 2x2 image with 2 colors
    # Top-left: Red, Top-right: Red
    # Bottom-left: Blue, Bottom-right: Blue
    img_data = np.zeros((2, 2, 3), dtype=np.uint8)
    img_data[0, 0] = [255, 0, 0] # Red
    img_data[0, 1] = [255, 0, 0] # Red
    img_data[1, 0] = [0, 0, 255] # Blue
    img_data[1, 1] = [0, 0, 255] # Blue

    img = Image.fromarray(img_data)
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    content = buf.getvalue()

    metrics = process_image(content)

    assert metrics["total_pixels"] == 4
    assert metrics["unique_color_count"] == 2
    assert metrics["width"] == 2
    assert metrics["height"] == 2

    assert len(metrics["top_colors"]) == 2
    # Both colors have equal count, order might vary but counts should be 2
    counts = [c["count"] for c in metrics["top_colors"]]
    assert counts == [2, 2]
    percentages = [c["percentage"] for c in metrics["top_colors"]]
    assert percentages == [50.0, 50.0]

def test_process_image_gradient():
    # Create a 10x10 image with unique colors (if possible)
    # Actually just 3 strips
    img_data = np.zeros((10, 10, 3), dtype=np.uint8)
    img_data[:5, :, :] = [255, 0, 0] # 50 pixels Red
    img_data[5:8, :, :] = [0, 255, 0] # 30 pixels Green
    img_data[8:, :, :] = [0, 0, 255] # 20 pixels Blue

    img = Image.fromarray(img_data)
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    content = buf.getvalue()

    metrics = process_image(content)

    assert metrics["total_pixels"] == 100
    assert metrics["unique_color_count"] == 3

    top_colors = metrics["top_colors"]
    assert top_colors[0]["hex"] == "#ff0000"
    assert top_colors[0]["count"] == 50
    assert top_colors[1]["hex"] == "#00ff00"
    assert top_colors[1]["count"] == 30
    assert top_colors[2]["hex"] == "#0000ff"
    assert top_colors[2]["count"] == 20
