import streamlit as st
from phi.agent import Agent
from phi.model.google import Gemini
from phi.tools.duckduckgo import DuckDuckGo
from google.generativeai import upload_file, get_file
import google.generativeai as genai
import time
from pathlib import Path
import tempfile
from dotenv import load_dotenv
import os

# Load environment variables and configure API
load_dotenv()
API_KEY = os.getenv("GOOGLE_API_KEY")
if API_KEY:
    genai.configure(api_key=API_KEY)
else:
    st.error("Google API Key not found. Please check your environment variables.")
    st.stop()

# Page configuration
st.set_page_config(
    page_title="Multimodal AI Video Analyzer",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
    <style>
    .main-header {
        font-family: 'Helvetica Neue', sans-serif;
        background: linear-gradient(90deg, #4b6cb7 0%, #182848 100%);
        background-clip: text;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .stTextArea textarea {
        height: 120px;
        font-size: 16px;
    }
    .stButton>button {
        background-color: #4b6cb7;
        color: white;
        border-radius: 8px;
        padding: 12px 24px;
        font-weight: bold;
        border: none;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        background-color: #182848;
        transform: translateY(-2px);
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .results-container {
        padding: 20px;
        border-radius: 10px;
        background-color: #f8f9fa;
        border-left: 5px solid #4b6cb7;
    }
    .upload-section {
        padding: 20px;
        border-radius: 10px;
        background-color: #f1f3f5;
        margin-bottom: 20px;
    }
    </style>
""", unsafe_allow_html=True)

# App header
st.markdown("<h1 class='main-header'>Video AI Summarizer Agent</h1>", unsafe_allow_html=True)
st.markdown("### 🎬 Powered by Gemini 2.0 Flash Exp & Phidata")

# Sidebar with information
with st.sidebar:
    st.markdown("## About This Tool")
    st.markdown("""
    This AI-powered tool analyzes videos and provides intelligent insights based on your questions.
    
    **Features:**
    - 🎥 Video content analysis
    - 🔍 Context-aware responses
    - 🌐 Web research integration
    - 📊 Detailed summaries
    
    **How to use:**
    1. Upload a video file
    2. Ask a specific question
    3. Get AI-powered insights
    """)
    
    st.markdown("---")
    st.markdown("#### 💡 Example Questions")
    st.markdown("""
    - Summarize the key points in this video
    - What techniques are being demonstrated?
    - Analyze the presentation style
    - Extract the main argument
    """)

# Initialize the agent
@st.cache_resource
def initialize_agent():
    return Agent(
        name="Video AI Summarizer",
        model=Gemini(id="gemini-2.0-flash-exp"),
        tools=[DuckDuckGo()],
        markdown=True,
    )

multimodal_Agent = initialize_agent()

# Main app layout
tabs = st.tabs(["Video Analysis", "History", "Help"])

with tabs[0]:
    col1, col2 = st.columns([3, 2])
    
    with col1:
        st.markdown("<div class='upload-section'>", unsafe_allow_html=True)
        st.subheader("📤 Upload Video")
        video_file = st.file_uploader(
            "Select a video file to analyze",
            type=['mp4', 'mov', 'avi'],
            help="Supported formats: MP4, MOV, AVI (max 200MB)"
        )
        
        if video_file:
            file_details = {"Filename": video_file.name, 
                           "FileType": video_file.type,
                           "FileSize": f"{round(video_file.size / (1024 * 1024), 2)} MB"}
            
            st.success(f"✅ File uploaded successfully: **{video_file.name}**")
            st.write(file_details)
            
            with tempfile.NamedTemporaryFile(delete=False, suffix='.mp4') as temp_video:
                temp_video.write(video_file.read())
                video_path = temp_video.name
            
            st.video(video_path, format="video/mp4", start_time=0)
        else:
            st.info("👆 Please upload a video file to begin analysis")
        st.markdown("</div>", unsafe_allow_html=True)
    
    with col2:
        if video_file:
            st.subheader("🔎 Analysis Options")
            analysis_type = st.radio(
                "Select analysis approach:",
                ["General Summary", "Specific Question"],
                help="Choose how you want to analyze the video"
            )
            
            if analysis_type == "General Summary":
                user_query = "Provide a comprehensive summary of this video, including main topics, key points, and overall message."
                st.info("AI will generate a general summary of the video content")
            else:
                user_query = st.text_area(
                    "What insights are you seeking from the video?",
                    placeholder="Ask a specific question about the video content...",
                    help="Be specific to get the most relevant insights"
                )
            
            analysis_depth = st.select_slider(
                "Analysis Depth",
                options=["Quick", "Standard", "Detailed"],
                value="Standard",
                help="Controls the thoroughness of the analysis"
            )
            
            web_research = st.checkbox("Enable web research for additional context", value=True)
            
            analyze_button = st.button("🔍 Analyze Video", key="analyze_video_button", use_container_width=True)
            
            if analyze_button:
                if not user_query:
                    st.warning("⚠️ Please enter a question or select General Summary")
                else:
                    try:
                        progress_bar = st.progress(0)
                        status_text = st.empty()
                        
                        # Simulate processing steps with progress updates
                        status_text.text("Initializing video processing...")
                        progress_bar.progress(10)
                        time.sleep(0.5)
                        
                        status_text.text("Uploading video for AI analysis...")
                        progress_bar.progress(30)
                        processed_video = upload_file(video_path)
                        
                        status_text.text("Processing video frames and audio...")
                        progress_bar.progress(50)
                        
                        while processed_video.state.name == "PROCESSING":
                            time.sleep(1)
                            processed_video = get_file(processed_video.name)
                        
                        status_text.text("Analyzing content and gathering insights...")
                        progress_bar.progress(70)
                        
                        # Build prompt based on user selections
                        depth_instructions = {
                            "Quick": "Provide a concise response focusing on the most important aspects.",
                            "Standard": "Provide a balanced analysis with moderate detail.",
                            "Detailed": "Provide an in-depth analysis with comprehensive details and nuanced observations."
                        }
                        
                        web_instructions = "Use web research to supplement your analysis with relevant external context." if web_research else "Focus only on video content without external research."
                        
                        analysis_prompt = f"""
                        Analyze the uploaded video for content and context.
                        {depth_instructions[analysis_depth]}
                        {web_instructions}
                        
                        Respond to the following query using video insights:
                        {user_query}
                        
                        Provide a structured, user-friendly, and actionable response.
                        """
                        
                        status_text.text("Generating final response...")
                        progress_bar.progress(90)
                        
                        # AI agent processing
                        response = multimodal_Agent.run(analysis_prompt, videos=[processed_video])
                        
                        # Complete progress
                        progress_bar.progress(100)
                        status_text.text("Analysis complete!")
                        time.sleep(0.5)
                        status_text.empty()
                        progress_bar.empty()
                        
                        # Display the result
                        st.markdown("<div class='results-container'>", unsafe_allow_html=True)
                        st.subheader("📊 Analysis Results")
                        st.markdown(response.content)
                        st.markdown("</div>", unsafe_allow_html=True)
                        
                    except Exception as error:
                        st.error(f"❌ An error occurred during analysis: {error}")
                    finally:
                        # Clean up temporary video file
                        Path(video_path).unlink(missing_ok=True)

with tabs[1]:
    st.markdown("### 📜 Analysis History")
    st.info("Your video analysis history will appear here")
    st.markdown("No previous analyses found. History will be saved after your first analysis.")

with tabs[2]:
    st.markdown("### ❓ Help & FAQ")
    
    faq = {
        "What types of videos work best?": "This tool works well with presentations, tutorials, interviews, lectures, and other content-rich videos. Videos under 10 minutes generally provide the most focused results.",
        "How detailed can my questions be?": "Very detailed! The more specific your question, the more targeted the AI's response will be. Example: Instead of 'What's in this video?' try 'How does the speaker support their argument about climate change?'",
        "Can it analyze videos in languages other than English?": "Yes, the system can analyze video content in multiple languages, though English content typically yields the most accurate results.",
        "Will my videos be stored?": "Videos are processed temporarily and then deleted after analysis. They are not permanently stored on our servers.",
        "What if I get an error?": "Common issues include file size limitations, unsupported formats, or connectivity problems. Try using a smaller video file or converting to MP4 format."
    }
    
    for question, answer in faq.items():
        with st.expander(question):
            st.write(answer)
    
    st.markdown("---")
    st.markdown("Need more help? Contact support@phidata.ai")

# Footer
st.markdown("---")
st.markdown("Built with ❤️ using Phidata & Streamlit | Gemini 2.0 Flash Exp")