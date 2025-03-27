# 📝 Weekly Reports Summarizer 

## 🌟 Overview

A powerful, intelligent weekly report summarization tool that transforms daily markdown reports into concise, insightful weekly summaries using AI technology.

![Project Banner](https://img.shields.io/badge/version-0.1.0-blue.svg)
![Python](https://img.shields.io/badge/python-3.8+-green.svg)
![AI Powered](https://img.shields.io/badge/AI-Gemini-orange.svg)

## ✨ Features

- 🤖 AI-powered weekly report summarization
- 📂 Supports markdown daily report files
- 🇧🇷 Portuguese-focused summarization
- 🔍 Configurable AI model and instructions
- 💾 Automatic summary file generation

## 🚀 Quick Start

### Prerequisites

- Python 3.9+
- Google Gemini API Key
- Daily markdown reports

### Installation

1. Clone the repository:
```bash
git clone https://github.com/guimaraesr-y/weekly-reports-summarizer.git
cd weekly-reports-summarizer
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Configure environment variables:
```bash
# Create a .env file
GEMINI_API_KEY=your_gemini_api_key
DEBUG=True  # Optional
```

### Usage

```bash
python weekly_summarizer.py
```

## 🔧 Configuration

Customize the summarizer through:
- `.env` file for API keys and settings
- Modify `ai/gemini.py` for different AI instructions
- Adjust `_get_weekly_reports()` method for specific report structures

## 📋 TODO

- [ ] Make the structure flexible and user-friendly via terminal.

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

Distributed under the MIT License. See `LICENSE` for more information.

---

**Made with ❤️ by Ryan Guimarães**