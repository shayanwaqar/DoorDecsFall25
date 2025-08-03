A python script to automate the creation of door decs. 

Created for use by Resident Assistants to make the name tags for each of their residents.


# Name Tag Generator

This script generates printable name tags using up to four base image templates and compiles them into a multi-page A4 landscape PDF (4 tags per page). Each name tag is saved as a PNG and also included in the final combined PDF with proper spacing for easy cutting.

---

## 📁 Folder Structure


.

├── base_images/

│   ├── base_image1.png

│   ├── base_image2.png

│   ├── base_image3.png

│   └── base_image4.png

├── fonts/

│   └── PressStart2P-Regular.ttf

├── generated_tags/           # Auto-created

├── names.txt

├── generate_tags.py

└── z_GENERATED_TAGS.pdf      # Final output

---
## 🛠 Requirements

- Python 3.x
- Pillow (`pip install pillow`)
---
## 🧾 Setup

1. Place your 4 base images in the `base_images/` folder.File names must be:

   - `base_image1.png`
   - `base_image2.png`
   - `base_image3.png`
   - `base_image4.png`
2. Create a `names.txt` file with one name per line.Skip the first line if it's a header (e.g., `First Name`).
3. Place the font file `PressStart2P-Regular.ttf` inside the `fonts/` folder.

---

## ▶️ How to Run

```bash
python generate_tags.py
```


## 📄 Output

* Individual PNG tags saved to `generated_tags/`
* Final multi-page PDF: `z_GENERATED_TAGS.pdf`
  * A4 landscape
  * 4 tags per page
  * Equal margins between tags for easier cutting

---

## 📝 Notes

* The script automatically adjusts the font size to fit long names within the tag.
* Each name cycles through the 4 base templates in order.
* Output is 300 DPI, suitable for high-quality printing.
* For new images, adjust the 'base_templates' to use a different x coordinate in the "pos".

## ✂️ Cutting Recommendation

The PDF layout includes padding between all tags, making it easy to cut with scissors or a paper cutter without overlapping neighboring tags.
