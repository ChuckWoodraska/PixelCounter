import io
from typing import Any

import numpy as np
from PIL import Image


def process_image(file_content: bytes) -> dict[str, Any]:
    """
    Process image bytes and return metrics about pixel colors.
    """
    image = Image.open(io.BytesIO(file_content))
    image = image.convert("RGB")

    # Convert to numpy array
    img_array = np.array(image)

    # Reshape to 2D array of pixels
    pixels = img_array.reshape(-1, 3)

    # Total pixel count
    total_pixels = pixels.shape[0]

    # Count unique colors
    # We can use numpy's unique to count, but it might be slow for large images with many colors.
    # A faster way for exact counting of RGB triplets is to view them as a structured array or void type
    # but simplest robust way is converting to tuples and using Counter if image is not huge,
    # OR using unique with axis=0.

    unique_colors, counts = np.unique(pixels, axis=0, return_counts=True)

    # Combine colors and counts
    # unique_colors is (N, 3), counts is (N,)

    # Sort by count descending
    sorted_indices = np.argsort(counts)[::-1]
    sorted_colors = unique_colors[sorted_indices]
    sorted_counts = counts[sorted_indices]

    # Prepare top 10 colors
    top_colors = []
    num_top = min(10, len(sorted_colors))

    for i in range(num_top):
        color = sorted_colors[i]
        count = sorted_counts[i]
        hex_color = f"#{color[0]:02x}{color[1]:02x}{color[2]:02x}"
        percentage = (count / total_pixels) * 100
        top_colors.append({
            "hex": hex_color,
            "rgb": f"rgb({color[0]}, {color[1]}, {color[2]})",
            "count": int(count),
            "percentage": round(percentage, 2)
        })

    return {
        "total_pixels": int(total_pixels),
        "unique_color_count": len(unique_colors),
        "top_colors": top_colors,
        "width": image.width,
        "height": image.height
    }
