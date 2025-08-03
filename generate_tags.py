from PIL import Image, ImageDraw, ImageFont
import os
from math import ceil

# Paths and settings
FONT_PATH = "fonts/PressStart2P-Regular.ttf"
OUTPUT_DIR = "generated_tags"
PDF_OUTPUT = "outputPDF.pdf"
NAME_FILE = "names.txt"

# Font and text
MAX_FONT_SIZE = 80
MIN_FONT_SIZE = 40
TEXT_COLOR = "white"
MAX_TEXT_WIDTH = 1000

# Page layout (A4 landscape at 300 DPI)
PAGE_WIDTH = 3508
PAGE_HEIGHT = 2480
CELL_MARGIN = 40

# Create output folder if it doesn't exist
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Load base images and their text positions
base_templates = [
    {"img": Image.open("base_images/base_image1.png"), "pos": (960, 475)},
    {"img": Image.open("base_images/base_image2.png"), "pos": (960, 500)},
    {"img": Image.open("base_images/base_image3.png"), "pos": (960, 500)},
    {"img": Image.open("base_images/base_image4.png"), "pos": (960, 425)},
]

# Read names (skip header row)
with open(NAME_FILE, "r") as f:
    names = [line.strip() for line in f if line.strip().lower() != "first name"]

tag_images = []

# Generate each tag
for i, name in enumerate(names):
    template = base_templates[i % 4]
    img = template["img"].copy()
    TEXT_POSITION = template["pos"]

    draw = ImageDraw.Draw(img)

    # Adjust font size to fit width
    font_size = MAX_FONT_SIZE
    while font_size >= MIN_FONT_SIZE:
        font = ImageFont.truetype(FONT_PATH, font_size)
        bbox = draw.textbbox((0, 0), name, font=font)
        text_width = bbox[2] - bbox[0]
        if text_width <= MAX_TEXT_WIDTH:
            break
        font_size -= 2

    text_height = bbox[3] - bbox[1]
    position = (
        TEXT_POSITION[0] - text_width // 2,
        TEXT_POSITION[1] - text_height // 2
    )

    draw.text(position, name, fill=TEXT_COLOR, font=font)

    # Save image
    output_path = os.path.join(OUTPUT_DIR, f"{name}.png")
    img.save(output_path, dpi=(300, 300))

    tag_images.append(img)

print(f"✅ Created {len(tag_images)} name tags in '{OUTPUT_DIR}'")

# Create PDF pages with 4 tags per page
GRID_ROWS = 2
GRID_COLS = 2

total_margin_x = (GRID_COLS + 1) * CELL_MARGIN
total_margin_y = (GRID_ROWS + 1) * CELL_MARGIN

cell_width = (PAGE_WIDTH - total_margin_x) // GRID_COLS
cell_height = (PAGE_HEIGHT - total_margin_y) // GRID_ROWS

pages = []

for i in range(0, len(tag_images), GRID_ROWS * GRID_COLS):
    page = Image.new("RGB", (PAGE_WIDTH, PAGE_HEIGHT), "white")

    for j, tag in enumerate(tag_images[i:i + GRID_ROWS * GRID_COLS]):
        row = j // GRID_COLS
        col = j % GRID_COLS

        # Resize with aspect ratio
        img_ratio = tag.width / tag.height
        cell_ratio = cell_width / cell_height

        if img_ratio > cell_ratio:
            new_height = cell_height
            new_width = int(new_height * img_ratio)
        else:
            new_width = cell_width
            new_height = int(new_width / img_ratio)

        resized = tag.resize((new_width, new_height), Image.Resampling.LANCZOS)

        # Center crop
        left = (new_width - cell_width) // 2
        top = (new_height - cell_height) // 2
        cropped = resized.crop((left, top, left + cell_width, top + cell_height))

        # Place on page
        x = col * (cell_width + CELL_MARGIN) + CELL_MARGIN
        y = row * (cell_height + CELL_MARGIN) + CELL_MARGIN
        page.paste(cropped, (x, y))

    pages.append(page)

# Save PDF
pages[0].save(PDF_OUTPUT, save_all=True, append_images=pages[1:], dpi=(300, 300))
print(f"📄 PDF saved as '{PDF_OUTPUT}' with {len(pages)} pages.")
