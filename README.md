# 🎬 Video AI Summarizer Agent

**An AI-powered video analysis tool that provides intelligent insights, summaries, and answers to user queries — all from uploaded video files.**

![App Screenshot](https://user-images.githubusercontent.com/demo_image.png)

## 🚀 Features

- 📤 Upload video files (MP4, MOV, AVI)
- 🤖 Analyze content using Google's Gemini 2.0 Flash Exp model
- 🌐 Optional web search with DuckDuckGo integration
- 📝 Ask general or specific questions about video content
- 📊 Select analysis depth (Quick, Standard, Detailed)
- 💡 Real-time UI with progress indicators and structured results

---

## 🛠️ Tech Stack

| Tool | Description |
|------|-------------|
| [Streamlit](https://streamlit.io) | Frontend UI for interactive apps |
| [Phidata](https://github.com/phidatahq) | LLM orchestration and agent framework |
| [Google Generative AI (Gemini)](https://ai.google.dev/) | Video analysis & LLM model |
| [DuckDuckGo Search Tool](https://duckduckgo.com/) | For contextual web research |
| `dotenv` | For environment variable handling |
| `tempfile`, `pathlib`, `os`, `time` | Python standard libraries |

---

## 🧠 How It Works

1. User uploads a video file
2. User selects analysis type: *General Summary* or *Specific Question*
3. AI agent processes the video and generates insights using:
   - Google's Gemini model
   - (Optional) DuckDuckGo web search
4. Streamlit displays the structured results with styled formatting

---

## 📦 Installation & Setup

### 1. Clone the repository

```bash
git clone https://github.com/your-username/multimodal-ai-video-analyzer.git
cd multimodal-ai-video-analyzer
