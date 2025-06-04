from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from io import BytesIO
from datetime import datetime
import base64
from PIL import Image as PILImage

def generate_pdf_report(inspection_id, images, analysis_text):
    """Generate a PDF report with the analysis results.
    
    Args:
        inspection_id: Unique ID for the inspection
        images: List of uploaded image files
        analysis_text: Text with the analysis results
    
    Returns:
        bytes: PDF content as bytes
    """
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    styles = getSampleStyleSheet()
    
    # Create custom styles
    title_style = ParagraphStyle(
        'Title',
        parent=styles['Heading1'],
        fontSize=18,
        alignment=1,
        spaceAfter=12
    )
    
    subtitle_style = ParagraphStyle(
        'Subtitle',
        parent=styles['Heading2'],
        fontSize=14,
        spaceAfter=6
    )
    
    normal_style = ParagraphStyle(
        'Normal',
        parent=styles['Normal'],
        fontSize=10,
        spaceAfter=6
    )
    
    # Create content elements
    elements = []
    
    # Add header
    elements.append(Paragraph("RELATÓRIO DE VISTORIA VEICULAR", title_style))
    elements.append(Spacer(1, 0.25*inch))
    
    # Add inspection details
    current_date = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    elements.append(Paragraph(f"ID da Vistoria: {inspection_id}", normal_style))
    elements.append(Paragraph(f"Data: {current_date}", normal_style))
    elements.append(Spacer(1, 0.25*inch))
    
    # Add images section
    elements.append(Paragraph("IMAGENS ANALISADAS", subtitle_style))
    elements.append(Spacer(1, 0.1*inch))
    
    # Process and add images
    for i, img_file in enumerate(images):
        if i % 2 == 0:
            # Start a new row for every 2 images
            if i > 0:
                elements.append(Spacer(1, 0.2*inch))
        
        # Process image
        img_data = img_file.getvalue()
        img = PILImage.open(BytesIO(img_data))
        
        # Resize image to fit in the report
        max_width = 250
        max_height = 200
        img.thumbnail((max_width, max_height))
        
        # Save the resized image
        img_buffer = BytesIO()
        img.save(img_buffer, format=img.format)
        img_buffer.seek(0)
        
        # Add image to report with centered caption
        img_obj = Image(img_buffer)
        img_obj.drawHeight = 2*inch
        img_obj.drawWidth = 2.5*inch
        
        # Create centered style for image caption
        centered_style = ParagraphStyle(
            'Centered',
            parent=styles['Normal'],
            fontSize=10,
            alignment=1,  # 1 = center alignment
            spaceAfter=6
        )
        
        elements.append(img_obj)
        elements.append(Paragraph(f"Imagem {i+1}: {img_file.name}", centered_style))
        elements.append(Spacer(1, 0.1*inch))
    
    # Add analysis section
    elements.append(Spacer(1, 0.25*inch))
    elements.append(Paragraph("LAUDO TÉCNICO", subtitle_style))
    elements.append(Spacer(1, 0.1*inch))
    
    # Split analysis text into paragraphs and add them
    paragraphs = analysis_text.split('\n\n')
    for para in paragraphs:
        if para.strip():
            # Remove ** markdown and apply bold with HTML tags
            formatted_para = para.replace('**', '')
            
            # Check if this is a heading (starts with # or ##)
            if para.strip().startswith('#'):
                heading_style = ParagraphStyle(
                    'Heading',
                    parent=styles['Heading3'],
                    fontSize=12,
                    spaceAfter=6,
                    spaceBefore=12
                )
                # Remove # symbols
                clean_para = para.strip().replace('#', '').strip()
                elements.append(Paragraph(f"<b>{clean_para}</b>", heading_style))
            else:
                elements.append(Paragraph(formatted_para.replace('\n', '<br/>'), normal_style))
            
            elements.append(Spacer(1, 0.1*inch))
    
    # Add footer
    elements.append(Spacer(1, 0.5*inch))
    elements.append(Paragraph("Este relatório foi gerado automaticamente pelo sistema VistoCarroAI de Vistoria Veicular.", 
                             ParagraphStyle('Footer', parent=styles['Normal'], fontSize=8, alignment=1)))
    
    # Build PDF
    doc.build(elements)
    buffer.seek(0)
    
    return buffer.getvalue()

def generate_txt_report(analysis_text):
    """Generate a TXT report with the key points of the analysis.
    
    Args:
        analysis_text: Text with the analysis results
    
    Returns:
        str: TXT content as string
    """
    current_date = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    
    # Create report content
    report = f"""RELATÓRIO DE VISTORIA VEICULAR - PONTOS-CHAVE
Data: {current_date}

{analysis_text}

---
Relatório gerado automaticamente pelo sistema VistoCarroAI de Vistoria Veicular.
"""
    
    return report