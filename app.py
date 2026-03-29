from flask import Flask, request, send_file, jsonify
import fitz  # PyMuPDF
from PIL import Image
import io
import os

app = Flask(__name__)

# Limit file size to 10MB
app.config['MAX_CONTENT_LENGTH'] = 10 * 1024 * 1024

@app.route('/')
def index():
    # Serve the frontend HTML file
    try:
        with open(os.path.join(os.path.dirname(__file__), 'index.html'), 'r') as f:
            content = f.read()
        return content, 200, {'Content-Type': 'text/html'}
    except Exception as e:
        return str(e), 500

@app.route('/convert', methods=['POST'])
def convert_pdf_to_image():
    # Check if file is present
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400
    
    file = request.files['file']
    
    # Check if file is selected
    if not file.filename or file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    # Check if file is PDF
    if not file.filename.lower().endswith('.pdf'):
        return jsonify({'error': 'Only PDF files are allowed'}), 400
    
    try:
        # Read PDF file
        pdf_bytes = file.read()
        pdf_document = fitz.open(stream=pdf_bytes, filetype="pdf")
        
        # Convert each page to image
        images = []
        for page_num in range(len(pdf_document)):
            page = pdf_document.load_page(page_num)
            # Render page to image (200 DPI for good quality)
            pix = page.get_pixmap(matrix=fitz.Matrix(200/72, 200/72))
            img_data = pix.tobytes("png")
            img = Image.open(io.BytesIO(img_data))
            images.append(img)
        
        pdf_document.close()
        
        if not images:
            return jsonify({'error': 'No pages found in PDF'}), 400
        
        # Calculate dimensions for merged image
        max_width = max(img.width for img in images)
        total_height = sum(img.height for img in images)
        
        # Create new image with white background
        merged_image = Image.new('RGB', (max_width, total_height), color='white')
        
        # Paste each image vertically
        y_offset = 0
        for img in images:
            # Calculate x offset to center the image if it's narrower than max_width
            x_offset = (max_width - img.width) // 2
            merged_image.paste(img, (x_offset, y_offset))
            y_offset += img.height
        
        # Save merged image to bytes
        img_io = io.BytesIO()
        merged_image.save(img_io, format='PNG')
        img_io.seek(0)
        
        # Return image as downloadable file
        return send_file(
            img_io,
            mimetype='image/png',
            as_attachment=True,
            download_name='converted.png'
        )
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    # For development only - use gunicorn for production
    app.run(host='0.0.0.0', port=5000, debug=True)