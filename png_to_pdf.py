from PIL import Image
import os
import math

# === SETTINGS ===
INPUT_FOLDER = "generated_tags"
OUTPUT_FILE = "y_tags.pdf"
PAGE_SIZE = (3508, 2480)  # A4 at 300 dpi, PORTRAIT
GRID_ROWS, GRID_COLS = 2, 2  # 4 per page

# Get all PNG files from the folder, sorted by name
png_files = sorted([f for f in os.listdir(INPUT_FOLDER) if f.endswith(".png")])

if not png_files:
    raise ValueError("❌ No PNG files found in the output folder.")

# Page layout calculations
cell_width = PAGE_SIZE[0] // GRID_COLS
cell_height = PAGE_SIZE[1] // GRID_ROWS

pages = []
for page_idx in range(math.ceil(len(png_files) / (GRID_ROWS * GRID_COLS))):
    # Create a blank white page
    page = Image.new("RGB", PAGE_SIZE, "white")

    for i in range(GRID_ROWS * GRID_COLS):
        img_idx = page_idx * (GRID_ROWS * GRID_COLS) + i
        if img_idx >= len(png_files):
            break

        img_path = os.path.join(INPUT_FOLDER, png_files[img_idx])
        img = Image.open(img_path).convert("RGB")

        # Resize image to fit cell (preserve aspect ratio)
        img.thumbnail((cell_width, cell_height), Image.Resampling.LANCZOS)

        # Calculate position to center image in cell
        row, col = divmod(i, GRID_COLS)
        x = col * cell_width + (cell_width - img.width) // 2
        y = row * cell_height + (cell_height - img.height) // 2

        page.paste(img, (x, y))

    pages.append(page)

# Save as multi-page PDF
pages[0].save(OUTPUT_FILE, save_all=True, append_images=pages[1:])
print(f"✅ Combined {len(png_files)} PNGs into '{OUTPUT_FILE}' with 4 per portrait page!")
