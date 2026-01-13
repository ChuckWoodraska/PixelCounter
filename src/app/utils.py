import io
import base64
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
    unique_colors, counts = np.unique(pixels, axis=0, return_counts=True)

    # Sort by count descending
    sorted_indices = np.argsort(counts)[::-1]
    sorted_colors = unique_colors[sorted_indices]
    sorted_counts = counts[sorted_indices]

    # Prepare top 25 colors
    top_colors = []
    num_top = min(25, len(sorted_colors))

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

    # Encode original image
    buffered = io.BytesIO()
    image.save(buffered, format="PNG")
    original_b64 = base64.b64encode(buffered.getvalue()).decode("utf-8")

    # --- Transformation 1: Quantize to Top 25 ---
    # Top colors (RGB array)
    top_colors_arr = sorted_colors[:num_top] # Shape (num_top, 3)

    # Initialize distances and indices
    # We want to map every pixel to the index of the closest top color
    # Tie breaking: prefer lower index (more frequent)

    # Because 'pixels' can be large, we avoid creating (N, 25, 3) array.
    # We iterate over the 25 colors.

    N = pixels.shape[0]
    # Initialize min_dists with infinity
    min_dists = np.full(N, np.inf, dtype=np.float32)
    # Initialize closest_indices with 0 (default, but will be overwritten)
    closest_indices = np.zeros(N, dtype=int)

    # Convert pixels to float for distance calc (avoid overflow on uint8 subtraction)
    pixels_float = pixels.astype(np.float32)
    top_colors_float = top_colors_arr.astype(np.float32)

    for i in range(num_top):
        color = top_colors_float[i]
        # Calculate squared Euclidean distance (no need for sqrt for comparison)
        # axis=1 sum over R,G,B
        dists = np.sum((pixels_float - color)**2, axis=1)

        # Update where new distance is strictly less than current min
        # Strict inequality ensures we keep the earlier (more frequent) color in case of ties
        mask = dists < min_dists
        min_dists[mask] = dists[mask]
        closest_indices[mask] = i

    # Map indices back to colors
    quantized_pixels = top_colors_arr[closest_indices]

    # Reconstruct image
    quantized_img_array = quantized_pixels.reshape((image.height, image.width, 3)).astype(np.uint8)
    quantized_image = Image.fromarray(quantized_img_array)

    buffered_quant = io.BytesIO()
    quantized_image.save(buffered_quant, format="PNG")
    quantized_b64 = base64.b64encode(buffered_quant.getvalue()).decode("utf-8")

    # --- Transformation 2: Top 25 to White ---
    # Create mask where pixels match any of the top colors
    # We can reuse the loop or do it efficiently.
    # Since we have closest_indices and min_dists,
    # if a pixel MATCHES a top color, min_dists should be 0.

    white_img_array = img_array.copy() # (H, W, 3)
    white_img_flat = white_img_array.reshape(-1, 3)

    # Check if min_dists is 0. But floats can be tricky.
    # Better to check strict equality with integer arithmetic or small epsilon.
    # Actually, simpler logic: check if pixel is in top_colors set.
    # But checking set membership for N pixels is O(N * 25).
    # We already computed distances. If distance is 0, it matches.

    match_mask = min_dists == 0
    # Apply white (255, 255, 255) to matching pixels
    white_img_flat[match_mask] = [255, 255, 255]

    # Reconstruct
    white_image = Image.fromarray(white_img_array)

    buffered_white = io.BytesIO()
    white_image.save(buffered_white, format="PNG")
    white_b64 = base64.b64encode(buffered_white.getvalue()).decode("utf-8")

    return {
        "total_pixels": int(total_pixels),
        "unique_color_count": len(unique_colors),
        "top_colors": top_colors,
        "width": image.width,
        "height": image.height,
        "original_image": original_b64,
        "quantized_image": quantized_b64,
        "white_image": white_b64
    }
