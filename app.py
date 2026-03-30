import gradio as gr
import fitz  # PyMuPDF
from PIL import Image
import io
import os

def convert_pdf_to_image(file):
    # Gradio provides file objects as TemporaryFilePath or NamedTemporaryFile-like
    if file is None:
        return None, "Please upload a PDF file."
    
    try:
        # Open PDF file using path provided by Gradio
        pdf_document = fitz.open(file.name)
        
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
            return None, "No pages found in PDF."
        
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
        
        # Return merged image and success message
        # Gradio can handle PIL image objects directly
        return merged_image, "Conversion successful! You can now download the image below."
        
    except Exception as e:
        return None, f"Error: {str(e)}"

# Custom Theme and Styling for Premium Look
# Using Soft theme with clean typography
with gr.Blocks(theme=gr.themes.Soft(primary_hue="blue"), title="PDF to Image Converter") as demo:
    gr.Markdown("""
    # 📄 PDF to Single Image Converter
    Upload a PDF file to convert all its pages into a single high-quality vertical image. Perfect for long documents!
    """)
    
    with gr.Row():
        with gr.Column(scale=1):
            input_pdf = gr.File(label="Upload PDF", file_types=[".pdf"])
            convert_btn = gr.Button("Convert Now", variant="primary")
            
        with gr.Column(scale=2):
            output_image = gr.Image(label="Converted Image", type="pil", show_download_button=True)
            status_msg = gr.Textbox(label="Status", value="Waiting for input...", interactive=False)
    
    # Connect input and output
    convert_btn.click(
        fn=convert_pdf_to_image,
        inputs=[input_pdf],
        outputs=[output_image, status_msg]
    )
    
    gr.Markdown("""
    ---
    *Built with Python, PyMuPDF, and Gradio. Best Performance on Hugging Face Spaces.*
    """)

if __name__ == "__main__":
    # In HF Spaces, this will run with demo.launch() automatically if you use the Gradio SDK
    demo.launch()