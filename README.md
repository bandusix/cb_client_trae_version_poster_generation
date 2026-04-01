# Capybaba AI Search - Trae Auto Poster Generator

[中文文档 / Chinese version](README_zh.md)

This is an automated poster generation script designed to quickly create high-quality promotional posters featuring an image grid, brand icon, adaptively typeset main title, and a Call-To-Action (CTA) button. It is specially designed for API integration, batch processing, and cross-language backend calls.

## 🎨 Theme Color Previews

The script supports random selection or explicit designation of theme colors. Below are the 6 built-in premium gradient presets:

| Red/Pink (`#FF6A7A`) | Light Blue (`#6A8BFF`) | Light Green (`#6AFF8B`) |
| :---: | :---: | :---: |
| <img src="docs_assets/preview_Red_Pink.png" width="300"> | <img src="docs_assets/preview_Light_Blue.png" width="300"> | <img src="docs_assets/preview_Light_Green.png" width="300"> |

| Light Yellow (`#FFD16A`) | Light Purple (`#B56AFF`) | Light Gray (`#8A95A5`) |
| :---: | :---: | :---: |
| <img src="docs_assets/preview_Light_Yellow.png" width="300"> | <img src="docs_assets/preview_Light_Purple.png" width="300"> | <img src="docs_assets/preview_Light_Gray.png" width="300"> |

---

## 🌟 Core Features
- **Highly Adaptive Typography**: Regardless of the title length or language, the script automatically adjusts the font size to fit the canvas, ensuring text never overlaps or gets truncated.
- **Smart Center Alignment**: Achieves precise horizontal visual centering for texts and icons using character metrics (Ascent / Descent).
- **Auto Theme Coloring**: If not specified, the script randomly picks from 6 high-quality light gradient backgrounds. You can also specify custom theme colors.
- **Robust Download Mechanism**: Built-in network timeout retries and exception handling prevent the entire process from crashing due to a single broken image link.
- **Flexible Integration**: Supports local calls, command-line arguments via JSON file, or direct JSON string passing.

---

## 🛠️ Parameters

Regardless of the calling method, the underlying data structure (JSON/Dict) expects the following parameters:

| Parameter | Type | Required | Description | Example |
| :--- | :--- | :--- | :--- | :--- |
| `icon_url` | String | No | Top-left brand icon. URL or local absolute path | `"https://capybaba.io/favicon.png"` |
| `brand_text` | String | No | Brand text right next to the icon | `"capybaba.io"` |
| `main_text` | String | Yes | Left main title. Use `\n` for line breaks | `"Top 10\nComedy\nMovies & TV\nShows"` |
| `cta_url` | String | No | Bottom-left CTA play/action icon | `"assets/play_icon.png"` |
| `cta_text` | String | No | Action text next to the CTA icon | `"Watch Now"` |
| `poster_urls` | Array | Yes | Array of poster images to display on the right (9~10 recommended) | `["https://xxx/1.jpg", "https://xxx/2.jpg"]` |
| `output_path` | String | No | Path/name to save the generated poster | `"output_poster.png"` |
| `theme_color` | String | No | [Optional] Custom gradient background color (Hex). Randomly chosen if omitted | `"#FF6A7A"` |

---

## 🚀 Integration Examples

### Method 1: Via JSON Config File (Recommended for Batch)
Save parameters as a `.json` file and run:
```bash
python3 trae_poster_generator.py --config data.json
```

### Method 2: Via JSON String (Recommended for Non-Python Backends)
If you use Node.js, Go, PHP, etc., you can execute system commands (`exec`) passing the serialized JSON string directly:
```bash
python3 trae_poster_generator.py --json '{
    "icon_url": "https://capybaba.io/favicon-128x128.png",
    "brand_text": "capybaba.io",
    "main_text": "Top 10\nComedy\nMovies & TV\nShows",
    "cta_url": "assets/play_icon.png",
    "cta_text": "Watch Now",
    "poster_urls": ["url1", "url2"]
}'
```

### Method 3: Direct Python Module Call (Recommended for Python Backends)
For frameworks like Django or FastAPI, simply `import` and pass a dictionary:
```python
from trae_poster_generator import generate_poster

payload = {
    "icon_url": "https://capybaba.io/favicon-128x128.png",
    "brand_text": "capybaba.io",
    "main_text": "Top 10\nComedy\nMovies & TV\nShows",
    "cta_url": "assets/play_icon.png",
    "cta_text": "Watch Now",
    "poster_urls": ["url1", "url2"]
}

generate_poster(**payload)
```