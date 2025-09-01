import streamlit as st
import numpy as np
import os
from PIL import Image, ImageEnhance, ImageFilter
import io
import tempfile
from gtts import gTTS
import fitz  # PyMuPDF

# ---------------- Config ----------------
SUPPORTED_FORMATS = ["jpg","jpeg","png","webp","pdf","txt","doc","docx"]
MAX_FILE_SIZE = 10*1024*1024

# ---------------- Professional Styling ----------------
def apply_legal_portal_styling():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    * {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    }
    
    .main .block-container {
        padding: 2rem 3rem;
        background: linear-gradient(135deg, #0F172A 0%, #1E293B 50%, #334155 100%);
        min-height: 100vh;
        color: white;
    }
    
    .main h1 {
        color: #F8FAFC !important;
        text-align: center;
        font-weight: 700;
        font-size: 2.5rem;
        margin-bottom: 1.5rem;
        letter-spacing: -0.025em;
    }
    
    .main h2, .main h3 {
        color: #3B82F6 !important;
        font-weight: 600;
        border-left: 4px solid #3B82F6;
        padding-left: 1rem;
        margin: 2rem 0 1rem 0;
    }
    
    .feature-list {
        background: linear-gradient(145deg, rgba(255,255,255,0.08), rgba(255,255,255,0.03));
        padding: 1.5rem;
        border-radius: 12px;
        border: 1px solid rgba(255,255,255,0.1);
        margin: 1.5rem 0;
    }
    
    .feature-list ul {
        margin: 0;
        padding-left: 1.5rem;
    }
    
    .feature-list li {
        color: #CBD5E1;
        margin: 0.5rem 0;
        line-height: 1.6;
    }
    
    .stButton > button {
        background: linear-gradient(135deg, #3B82F6 0%, #1D4ED8 100%) !important;
        color: white !important;
        font-weight: 600;
        font-size: 1rem;
        border: none !important;
        border-radius: 12px !important;
        padding: 0.875rem 2rem !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        box-shadow: 0 4px 12px rgba(59, 130, 246, 0.3) !important;
        letter-spacing: 0.025em !important;
        width: 100% !important;
    }
    
    .stButton > button:hover {
        background: linear-gradient(135deg, #1D4ED8 0%, #1E40AF 100%) !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 20px rgba(59, 130, 246, 0.4) !important;
    }
    
    .stTextArea > div > div > textarea {
        background: rgba(255,255,255,0.08) !important;
        color: #F8FAFC !important;
        border: 1px solid rgba(255,255,255,0.2) !important;
        border-radius: 8px !important;
    }
    
    .stSuccess, .stInfo, .stWarning, .stError {
        border-radius: 8px !important;
    }
    
    .summary-container {
        background: linear-gradient(145deg, rgba(255,255,255,0.08), rgba(255,255,255,0.03));
        padding: 1.5rem;
        border-radius: 12px;
        border: 1px solid rgba(59, 130, 246, 0.3);
        margin: 1rem 0;
    }
    
    .audio-section {
        background: linear-gradient(145deg, rgba(139, 92, 246, 0.1), rgba(139, 92, 246, 0.05));
        padding: 1.5rem;
        border-radius: 12px;
        border: 1px solid rgba(139, 92, 246, 0.2);
        margin: 1.5rem 0;
    }
    </style>
    """, unsafe_allow_html=True)

# ---------------- OCR ----------------
@st.cache_resource
def load_ocr_model():
    try:
        import easyocr
        return easyocr.Reader(['en'], gpu=False)
    except ImportError:
        st.error("EasyOCR not installed. Please install: pip install easyocr")
        return None
    except Exception as e:
        st.error(f"Error loading OCR model: {str(e)}")
        return None

def preprocess_image(image):
    """Enhanced image preprocessing for better OCR results"""
    if image.mode != 'RGB': 
        image = image.convert('RGB')
    
    width, height = image.size
    if width > 2000 or height > 2000:
        ratio = min(2000/width, 2000/height)
        new_size = (int(width * ratio), int(height * ratio))
        image = image.resize(new_size, Image.Resampling.LANCZOS)
    
    image = ImageEnhance.Contrast(image).enhance(1.5)
    image = ImageEnhance.Sharpness(image).enhance(1.3)
    image = image.convert('L')
    image = image.filter(ImageFilter.MedianFilter(size=3))
    
    return image

def extract_text_from_image(image, ocr_reader):
    """Extract text from image using OCR"""
    if ocr_reader is None:
        return "OCR model not available"
    
    try:
        processed = preprocess_image(image)
        arr = np.array(processed)
        results = ocr_reader.readtext(arr, detail=0, paragraph=True)
        return ' '.join(results).strip()
    except Exception as e:
        st.error(f"OCR extraction failed: {str(e)}")
        return ""

def extract_text_from_pdf(uploaded_file):
    """Extract text from PDF using PyMuPDF"""
    try:
        uploaded_file.seek(0)
        pdf_bytes = uploaded_file.read()
        pdf_document = fitz.open(stream=pdf_bytes, filetype="pdf")
        
        text = ""
        for page_num in range(pdf_document.page_count):
            page = pdf_document[page_num]
            text += page.get_text()
        
        pdf_document.close()
        return text.strip()
    
    except Exception as e:
        st.error(f"PDF extraction failed: {str(e)}")
        return ""

# ---------------- Summarizer ----------------
def simple_text_summarizer(text, max_sentences=3):
    """Simple rule-based summarizer as fallback"""
    if not text or len(text.strip()) < 100:
        return text
    
    sentences = [s.strip() for s in text.replace('\n', ' ').split('.') if s.strip()]
    
    if len(sentences) <= max_sentences:
        return text
    
    indices = [0, len(sentences)//2, -1]
    summary_sentences = [sentences[i] for i in indices if i < len(sentences)]
    
    return '. '.join(summary_sentences) + '.'

def summarize_text(text):
    """Summarize text with fallback options"""
    if not text or len(text.strip()) < 50:
        return text
    
    try:
        from transformers import pipeline
        summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
        
        max_length = 1000
        if len(text) > max_length:
            text = text[:max_length] + "..."
        
        summary = summarizer(text, max_length=120, min_length=30, do_sample=False)
        return summary[0]['summary_text']
    
    except ImportError:
        st.warning("Advanced summarizer not available. Using simple summarizer.")
        return simple_text_summarizer(text)
    except Exception as e:
        st.warning(f"Summarization error: {str(e)}. Using simple summarizer.")
        return simple_text_summarizer(text)

# ---------------- Legal Text Simplification ----------------
def simplify_legal_text(text):
    """Convert legal jargon to plain language"""
    replacements = {
        "whereas": "because",
        "heretofore": "before now",
        "hereafter": "from now on",
        "aforementioned": "mentioned above",
        "pursuant to": "according to",
        "notwithstanding": "despite",
        "hereinafter": "from now on called",
        "therefor": "for that reason",
        "whereby": "by which",
        "thereof": "of it",
        "therein": "in it",
        "party of the first part": "first party",
        "party of the second part": "second party",
    }
    
    simplified = text.lower()
    for legal_term, plain_term in replacements.items():
        simplified = simplified.replace(legal_term.lower(), plain_term)
    
    return simplified.capitalize()

# ---------------- Audio Guidance ----------------
def create_audio_summary(text, language='en'):
    """Create audio file from text"""
    try:
        if not text or len(text.strip()) == 0:
            return None
            
        tts = gTTS(text=text, lang=language, slow=False)
        tmp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
        tts.save(tmp_file.name)
        return tmp_file.name
    except Exception as e:
        st.error(f"Audio generation failed: {str(e)}")
        return None

def play_audio_summary(summary_text):
    """Play audio summary"""
    st.markdown('<div class="audio-section">', unsafe_allow_html=True)
    st.markdown("### Audio Summary")
    st.markdown("**English Audio:**")
    
    audio_file_en = create_audio_summary(summary_text, 'en')
    if audio_file_en:
        st.audio(audio_file_en, format="audio/mp3")
    else:
        st.caption("English audio unavailable")
    
    st.markdown('</div>', unsafe_allow_html=True)

# ---------------- Main App ----------------
def run():
    st.set_page_config(
        page_title="Legal Document Summarizer", 
        layout="wide",
        initial_sidebar_state="collapsed"
    )
    
    apply_legal_portal_styling()

    st.title("Legal Document Summarizer")
    
    st.markdown("""
    <div class="feature-list">
        <strong>Upload a legal document</strong> (PDF or image) and get:
        <ul>
            <li><strong>Text extraction</strong> from your document</li>
            <li><strong>Plain language summary</strong></li>
            <li><strong>Audio playback</strong> in multiple languages</li>
            <li><strong>Legal term simplification</strong></li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

    # Load OCR model
    ocr_reader = load_ocr_model()
    if ocr_reader is None:
        st.stop()

    # File uploader
    uploaded_file = st.file_uploader(
        "Choose a document file", 
        type=SUPPORTED_FORMATS,
        help="Supported formats: PDF, JPG, PNG, WEBP (Max 10MB)"
    )

    if uploaded_file is not None:
        # Check file size
        if uploaded_file.size > MAX_FILE_SIZE:
            st.error(f"File too large ({uploaded_file.size/1024/1024:.1f}MB). Maximum size is 10MB.")
            return

        # Show file info
        st.success(f"Uploaded: {uploaded_file.name} ({uploaded_file.size/1024:.1f}KB)")

        # Extract text based on file type
        with st.spinner("Extracting text from document..."):
            extracted_text = ""
            
            if uploaded_file.type == "application/pdf":
                extracted_text = extract_text_from_pdf(uploaded_file)
            elif uploaded_file.type == "text/plain" or uploaded_file.name.endswith('.txt'):
                try:
                    extracted_text = str(uploaded_file.read(), "utf-8")
                except Exception as e:
                    st.error(f"Failed to read text file: {str(e)}")
                    return
            else:
                try:
                    image = Image.open(uploaded_file)
                    st.image(image, caption="Document Preview", use_container_width=True)
                    extracted_text = extract_text_from_image(image, ocr_reader)
                except Exception as e:
                    st.error(f"Failed to process image: {str(e)}")
                    return

        # Display extracted text
        if extracted_text and len(extracted_text.strip()) > 0:
            word_count = len(extracted_text.split())
            st.info(f"Extracted {word_count} words from the document")

            # Summarization section
            if st.button("Generate Summary & Audio", type="primary"):
                with st.spinner("Creating summary..."):
                    summary = summarize_text(extracted_text)
                    simplified_summary = simplify_legal_text(summary)
                    
                    st.subheader("Document Summary")
                    st.success("Summary generated successfully!")
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        st.markdown('<div class="summary-container">', unsafe_allow_html=True)
                        st.markdown("**Original Summary:**")
                        st.write(summary)
                        st.markdown('</div>', unsafe_allow_html=True)
                    
                    with col2:
                        st.markdown('<div class="summary-container">', unsafe_allow_html=True)
                        st.markdown("**Simplified Version:**")
                        st.write(simplified_summary)
                        st.markdown('</div>', unsafe_allow_html=True)
                    
                    play_audio_summary(simplified_summary)
                    
        else:
            st.warning("No text could be extracted from the document. Please try:")
            st.markdown("""
            - Ensuring the image is clear and readable
            - Using a higher resolution scan
            - Checking that the document contains readable text
            - Trying a different file format
            """)

    # Sidebar instructions
    with st.sidebar:
        st.markdown("""
        ### How to Use This Tool

        **Instructions:**
        1. **Upload Document**: Choose a PDF or image file containing legal text
        2. **Review Extraction**: Check that the text was extracted correctly
        3. **Generate Summary**: Click the button to create a simplified summary
        4. **Listen**: Use the audio feature to hear the summary read aloud

        **Supported File Types:**
        - **PDF**: Text-based PDFs work best
        - **Images**: JPG, PNG, WEBP (scanned documents, photos)

        **Tips for Best Results:**
        - Use high-quality, clear images
        - Ensure text is horizontal and readable
        - PDF files generally give better text extraction than images
        """)

