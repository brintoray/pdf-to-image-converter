# PDF to Image Converter

A full-stack web application that converts PDF files into a single long vertical image.

## Features

- Modern, clean, responsive frontend using Tailwind CSS
- PDF file upload system with validation
- Automatic conversion and download of PNG image
- Error handling for invalid files and empty uploads
- Backend API endpoint: POST /convert
- Vertical image merging using Pillow
- Deployment-ready for Render and Netlify

## Quick Start

1. Clone this repository
2. Create virtual environment: `python3 -m venv venv`
3. Activate: `source venv/bin/activate`
4. Install dependencies: `pip install -r requirements.txt`
5. Run the app: `python app.py`
6. Visit http://localhost:5000

## Files

- `app.py` - Flask backend with PDF to image conversion
- `requirements.txt` - Dependencies (flask, pymupdf, pillow, gunicorn)
- `index.html` - Frontend with Tailwind CSS

## Deployment

### Backend (Render)
- Use gunicorn: `gunicorn app:app`
- Add `web: gunicorn app:app` to Procfile

### Frontend (Netlify)
- Upload index.html directly
- No build process required

## Usage

1. Upload a PDF file
2. Click "Convert" button
3. Wait for processing
4. Automatically download converted PNG image

## Requirements

- Python 3.8+
- PyMuPDF for PDF processing
- Pillow for image manipulation
- Flask for web framework