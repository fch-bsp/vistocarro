import streamlit as st
import os
import boto3
import json
import base64
import uuid
from datetime import datetime
from PIL import Image
import io
import numpy as np
from dotenv import load_dotenv
from utils.s3_handler import S3Handler
from utils.report_generator import generate_pdf_report, generate_txt_report
from utils.gemini_handler import GeminiHandler
from utils.image_analyzer_fallback import ImageAnalyzerFallback
from utils.default_analysis import DEFAULT_ANALYSIS

# Load environment variables
load_dotenv()

# Initialize handlers
s3_handler = S3Handler()
gemini_handler = GeminiHandler()
fallback_analyzer = ImageAnalyzerFallback()

# Set page configuration
st.set_page_config(
    page_title="VistoCarroAI - Sistema de Vistoria Veicular",
    page_icon="🚗",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main {
        background-color: #f5f7f9;
    }
    .stApp {
        background-image: url("https://images.unsplash.com/photo-1552519507-da3b142c6e3d?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=2070&q=80");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        background-attachment: fixed;
        background-color: rgba(255, 255, 255, 0.9);
        background-blend-mode: lighten;
    }
    .stSidebar {
        background-color: rgba(255, 255, 255, 0.9);
    }
    .css-1d391kg {
        padding: 2rem 1rem;
    }
    .stButton>button {
        background-color: #0066cc;
        color: white;
        border-radius: 5px;
        padding: 0.5rem 1rem;
        font-weight: bold;
    }
    .report-box {
        background-color: white;
        border-radius: 10px;
        padding: 20px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        margin-bottom: 20px;
    }
    .chat-message {
        padding: 1rem;
        border-radius: 10px;
        margin-bottom: 10px;
        display: flex;
        align-items: flex-start;
    }
    .user-message {
        background-color: #e6f3ff;
        margin-left: 20%;
    }
    .assistant-message {
        background-color: #f0f0f0;
        margin-right: 20%;
    }
</style>
""", unsafe_allow_html=True)

# Comment out the clear to maintain state between refreshes
# st.session_state.clear()

# Initialize session state
if 'uploaded_images' not in st.session_state:
    st.session_state.uploaded_images = []
if 'analysis_results' not in st.session_state:
    st.session_state.analysis_results = None
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'report_urls' not in st.session_state:
    st.session_state.report_urls = {'pdf': None, 'txt': None}
if 'inspection_id' not in st.session_state:
    st.session_state.inspection_id = str(uuid.uuid4())

# Sidebar
with st.sidebar:
    st.image("https://img.icons8.com/color/96/000000/car-crash.png", width=100)
    st.title("VistoCarroAI")
    st.subheader("Assistente de Vistoria Veicular")
    
    st.markdown("---")
    
    # Upload images
    st.subheader("📸 Upload de Imagens")
    uploaded_files = st.file_uploader("Carregue as imagens do veículo", 
                                     type=["jpg", "jpeg", "png"], 
                                     accept_multiple_files=True)
    
    if uploaded_files:
        st.session_state.uploaded_images = uploaded_files
        st.success(f"{len(uploaded_files)} imagens carregadas com sucesso!")
    
    # Analyze button
    if st.button("🔍 Analisar Imagens", disabled=len(st.session_state.uploaded_images) == 0):
        with st.spinner("Analisando imagens..."):
            # Process each image
            image_analyses = []
            
            for img_file in st.session_state.uploaded_images:
                # Read image
                img_bytes = img_file.getvalue()
                
                # Upload to S3
                img_key = f"uploads/{st.session_state.inspection_id}/{img_file.name}"
                s3_handler.upload_file_object(img_bytes, img_key)
                
                # Analyze image using Gemini with fallback
                with st.status(f"Analisando imagem {img_file.name}..."):
                    try:
                        # Try with Gemini first
                        analysis = gemini_handler.analyze_image(img_bytes)
                        st.success(f"Análise da imagem {img_file.name} concluída com sucesso!")
                    except Exception as e:
                        # If Gemini fails, use fallback analyzer
                        st.warning(f"API do Gemini indisponível: {str(e)}. Usando analisador local.")
                        analysis = fallback_analyzer.analyze_image(img_bytes)
                        st.success(f"Análise da imagem {img_file.name} concluída com analisador local!")
                    
                    # Add analysis to the list
                    image_analyses.append({
                        "filename": img_file.name,
                        "analysis": analysis
                    })
            
            # Generate combined analysis from all images
            with st.status("Gerando análise combinada..."):
                try:
                    # Try with Gemini first
                    combined_analysis = gemini_handler.generate_combined_analysis(image_analyses)
                    st.success("Análise combinada gerada com sucesso!")
                except Exception as e:
                    # If Gemini fails, use fallback analyzer
                    st.warning(f"API do Gemini indisponível: {str(e)}. Usando analisador local.")
                    combined_analysis = fallback_analyzer.generate_combined_analysis(image_analyses)
                    st.success("Análise combinada gerada com analisador local!")
                
                # Store the analysis results
                st.session_state.analysis_results = combined_analysis
            
            # Generate reports
            pdf_content = generate_pdf_report(st.session_state.inspection_id, 
                                             st.session_state.uploaded_images, 
                                             combined_analysis)
            txt_content = generate_txt_report(combined_analysis)
            
            # Upload reports to S3
            pdf_key = f"reports/{st.session_state.inspection_id}/report.pdf"
            txt_key = f"reports/{st.session_state.inspection_id}/report.txt"
            
            s3_handler.upload_file_object(pdf_content, pdf_key)
            s3_handler.upload_file_object(txt_content.encode('utf-8'), txt_key)
            
            # Generate presigned URLs for reports
            st.session_state.report_urls['pdf'] = s3_handler.get_presigned_url(pdf_key)
            st.session_state.report_urls['txt'] = s3_handler.get_presigned_url(txt_key)
            
            # Show success message
            st.success("Análise concluída com sucesso!")
    
    st.markdown("---")
    
    # Display report links if available
    if st.session_state.report_urls['pdf']:
        st.subheader("📄 Relatórios")
        st.markdown(f"[Baixar Relatório PDF]({st.session_state.report_urls['pdf']})")
        st.markdown(f"[Baixar Relatório TXT]({st.session_state.report_urls['txt']})")

# Main content
st.title("Sistema de Vistoria Veicular 🚗")

# Display uploaded images
if st.session_state.uploaded_images:
    st.header("Imagens Carregadas")
    cols = st.columns(3)
    for i, img_file in enumerate(st.session_state.uploaded_images):
        with cols[i % 3]:
            st.image(img_file, caption=img_file.name, use_column_width=True)

# Display analysis results
if st.session_state.analysis_results:
    st.header("Resultado da Análise")
    with st.container():
        st.markdown(f"""
        <div class="report-box">
            <h3>Laudo Técnico</h3>
            <p>{st.session_state.analysis_results}</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Chat with VistoCarroAI
    st.header("Consulte o Assistente VistoCarroAI")
    st.markdown("Faça perguntas sobre a vistoria e o assistente responderá com base na análise.")
    
    # Display chat history
    for message in st.session_state.chat_history:
        if message["role"] == "user":
            st.markdown(f"""
            <div class="chat-message user-message">
                <div>👤 <b>Você:</b> {message["content"]}</div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="chat-message assistant-message">
                <div>🤖 <b>Vistoriador:</b> {message["content"]}</div>
            </div>
            """, unsafe_allow_html=True)
    
    # Chat input form
    with st.form(key="chat_form", clear_on_submit=True):
        user_question = st.text_input("Digite sua pergunta para o Vistoriador:")
        submit_button = st.form_submit_button("Enviar")
        
        if submit_button and user_question:
            # Add user message to chat history
            st.session_state.chat_history.append({"role": "user", "content": user_question})
            
            # Get response from VistoCarroAI
            with st.spinner("Vistoriador está analisando..."):
                # Ensure we have analysis results
                analysis_text = st.session_state.analysis_results
                if analysis_text is None:
                    analysis_text = DEFAULT_ANALYSIS
                    
                response = gemini_handler.answer_question(user_question, analysis_text)
            
            # Add assistant response to chat history
            st.session_state.chat_history.append({"role": "assistant", "content": response})
            
            # Force a rerun to update the chat display
            st.rerun()
else:
    st.info("Carregue imagens e clique em 'Analisar Imagens' para iniciar a vistoria.")