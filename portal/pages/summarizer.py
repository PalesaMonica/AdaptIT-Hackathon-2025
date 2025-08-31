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

# ---------------- Styling ----------------
def apply_legal_portal_styling():
    st.markdown("""
    <style>
    :root {
        --justice-navy: #1E2A38;
        --justice-gold: #D4AF37;
        --justice-green: #2E8B57;
    }
    .main .block-container {
        padding: 2rem;
        background: linear-gradient(135deg, #1E2A38 0%, #2E8B57 100%);
        border-radius: 10px;
        color: white;
    }
    .main h1 {
        color: #D4AF37 !important;
        text-align: center;
        font-weight: bold;
    }
    .main h3 {
        color: #D4AF37 !important;
        border-left: 5px solid #D4AF37;
        padding-left: 10px;
    }
    .stButton > button {
        background: linear-gradient(45deg, #D4AF37, #FFD700) !important;
        color: #1E2A38 !important;
        font-weight: bold;
        border: none;
        border-radius: 8px;
        padding: 10px 20px;
    }
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
    }
    .stTextArea > div > div > textarea {
        background-color: rgba(255,255,255,0.1) !important;
        color: white !important;
    }
    </style>
    """, unsafe_allow_html=True)

# ---------------- OCR ----------------
@st.cache_resource
def load_ocr_model():
    try:
        import easyocr
        return easyocr.Reader(['en'], gpu=False)  # Removed 'af' as it may not be available
    except ImportError:
        st.error("EasyOCR not installed. Please install: pip install easyocr")
        return None
    except Exception as e:
        st.error(f"Error loading OCR model: {str(e)}")
        return None

def preprocess_image(image):
    """Enhanced image preprocessing for better OCR results"""
    # Convert to RGB if needed
    if image.mode != 'RGB': 
        image = image.convert('RGB')
    
    # Resize if image is too large (helps with OCR performance)
    width, height = image.size
    if width > 2000 or height > 2000:
        ratio = min(2000/width, 2000/height)
        new_size = (int(width * ratio), int(height * ratio))
        image = image.resize(new_size, Image.Resampling.LANCZOS)
    
    # Enhance contrast and sharpness
    image = ImageEnhance.Contrast(image).enhance(1.5)
    image = ImageEnhance.Sharpness(image).enhance(1.3)
    
    # Convert to grayscale
    image = image.convert('L')
    
    # Apply noise reduction
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
        # Reset file pointer
        uploaded_file.seek(0)
        
        # Read PDF using PyMuPDF
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
    
    # Split into sentences
    sentences = [s.strip() for s in text.replace('\n', ' ').split('.') if s.strip()]
    
    if len(sentences) <= max_sentences:
        return text
    
    # Take first, middle, and last sentences for a basic summary
    indices = [0, len(sentences)//2, -1]
    summary_sentences = [sentences[i] for i in indices if i < len(sentences)]
    
    return '. '.join(summary_sentences) + '.'

def summarize_text(text):
    """Summarize text with fallback options"""
    if not text or len(text.strip()) < 50:
        return text
    
    # Try Transformers summarization first
    try:
        from transformers import pipeline
        summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
        
        # Truncate text if too long (BART has token limits)
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
    # Common legal term replacements
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
    """Play audio summary in available languages"""
    st.markdown("### 🔊 Audio Summary")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**English Audio:**")
        audio_file_en = create_audio_summary(summary_text, 'en')
        if audio_file_en:
            st.audio(audio_file_en, format="audio/mp3")
        else:
            st.caption("English audio unavailable")
    
    with col2:
        st.markdown("**Afrikaans Audio:**")
        # Simple translation attempt for Afrikaans (basic approach)
        audio_file_af = create_audio_summary(summary_text, 'af')
        if audio_file_af:
            st.audio(audio_file_af, format="audio/mp3")
        else:
            st.caption("Afrikaans audio unavailable")

# ---------------- Main App ----------------
def run():
    st.set_page_config(
        page_title="Legal Document Summarizer", 
        layout="wide",
        initial_sidebar_state="collapsed"
    )
    
    apply_legal_portal_styling()

    st.title("📄 Legal Document Summarizer")
    st.markdown("""
    **Upload a legal document** (PDF or image) and get:
    - 📖 **Text extraction** from your document
    - 📝 **Plain language summary** 
    - 🔊 **Audio playback** in multiple languages
    - ⚖️ **Legal term simplification**
    """)

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
        st.success(f"✅ Uploaded: {uploaded_file.name} ({uploaded_file.size/1024:.1f}KB)")

        # Extract text based on file type
        with st.spinner("Extracting text from document..."):
            extracted_text = ""
            
            if uploaded_file.type == "application/pdf":
                extracted_text = extract_text_from_pdf(uploaded_file)
            elif uploaded_file.type == "text/plain" or uploaded_file.name.endswith('.txt'):
                # Handle TXT files
                try:
                    extracted_text = str(uploaded_file.read(), "utf-8")
                except Exception as e:
                    st.error(f"Failed to read text file: {str(e)}")
                    return
            else:
                # Handle image files
                try:
                    image = Image.open(uploaded_file)
                    st.image(image, caption="Document Preview", use_container_width=True)
                    extracted_text = extract_text_from_image(image, ocr_reader)
                except Exception as e:
                    st.error(f"Failed to process image: {str(e)}")
                    return

        # Display extracted text
        if extracted_text and len(extracted_text.strip()) > 0:
            st.subheader("📄 Extracted Text")
            with st.expander("View Full Extracted Text", expanded=False):
                st.text_area("Full Document Text", extracted_text, height=200, disabled=True)
            
            # Word count info
            word_count = len(extracted_text.split())
            st.info(f"📊 Extracted {word_count} words from the document")

            # Summarization section
            if st.button("🔍 Generate Summary & Audio", type="primary"):
                with st.spinner("Creating summary..."):
                    # Generate summary
                    summary = summarize_text(extracted_text)
                    
                    # Simplify legal language
                    simplified_summary = simplify_legal_text(summary)
                    
                    # Display results
                    st.subheader("📋 Document Summary")
                    st.success("Summary generated successfully!")
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        st.markdown("**Original Summary:**")
                        st.write(summary)
                    
                    with col2:
                        st.markdown("**Simplified Version:**")
                        st.write(simplified_summary)
                    
                    # Generate audio
                    play_audio_summary(simplified_summary)
                    
                    # Additional features
                    st.subheader("📊 Document Analysis")
                    col3, col4, col5 = st.columns(3)
                    with col3:
                        st.metric("Original Words", len(extracted_text.split()))
                    with col4:
                        st.metric("Summary Words", len(simplified_summary.split()))
                    with col5:
                        compression_ratio = len(simplified_summary.split()) / len(extracted_text.split()) * 100
                        st.metric("Compression", f"{compression_ratio:.1f}%")

        else:
            st.warning("⚠️ No text could be extracted from the document. Please try:")
            st.markdown("""
            - Ensuring the image is clear and readable
            - Using a higher resolution scan
            - Checking that the document contains readable text
            - Trying a different file format
            """)

    # Instructions section
    with st.expander("ℹ️ How to Use This Tool", expanded=False):
        st.markdown("""
        ### Instructions:
        1. **Upload Document**: Choose a PDF or image file containing legal text
        2. **Review Extraction**: Check that the text was extracted correctly
        3. **Generate Summary**: Click the button to create a simplified summary
        4. **Listen**: Use the audio feature to hear the summary read aloud
        
        ### Supported File Types:
        - **PDF**: Text-based PDFs work best
        - **Images**: JPG, PNG, WEBP (scanned documents, photos)
        
        ### Tips for Best Results:
        - Use high-quality, clear images
        - Ensure text is horizontal and readable
        - PDF files generally give better text extraction than images
        """)

