# Ollama Streamlit Chat Application

A modern, user-friendly chat interface for interacting with local Large Language Models (LLMs) through Ollama. This Streamlit application provides real-time streaming responses, model selection, and configurable chat settings.

![Python](https://img.shields.io/badge/python-v3.7+-blue.svg)  
![Streamlit](https://img.shields.io/badge/streamlit-v1.28.0+-red.svg)

## Features

- 🤖 **Multiple Model Support** - Automatically detects and allows selection of available Ollama models
- 💬 **Real-time Chat Interface** - Clean, intuitive chat UI with message history
- 🔄 **Streaming Responses** - Live streaming of model responses for better user experience
- ⚙️ **Configurable Settings** - Adjustable temperature control for response creativity
- 🔌 **Connection Monitoring** - Real-time connection status with Ollama service
- 🗑️ **Chat Management** - Clear chat history and session management
- 🚨 **Error Handling** - Comprehensive error handling and user feedback

## Installation

### Option 1: Clone from GitHub (Recommended)

```bash
git clone https://github.com/rush157/ollamabot.git
````

## Prerequisites

### 1. Ollama Installation

First, install Ollama on your system:

**Windows:**

```bash
# Download and install from https://ollama.ai/download
# Or use the installer script
```

**macOS:**

```bash
brew install ollama
```

**Linux:**

```bash
curl -fsSL https://ollama.ai/install.sh | sh
```

### 2. Start Ollama Service

```bash
ollama serve
```

### 3. Download Models

Pull at least one model to get started:

```bash
# Popular models (choose one or more)
ollama pull llama2          
ollama pull mistral         
ollama pull codellama       
ollama pull phi             
ollama pull neural-chat     
```

## Quick Start

### 1. Clone the Repository

```bash
git clone https://github.com/rush157/ollamabot.git
```

Or download the ZIP file from the repository and extract it.

### 2. Setup Virtual Environment

Simply run the setup script:

```cmd
create_venv.bat
```

This will:

* Create a virtual environment in `.venv` folder
* Activate the environment
* Install all required dependencies

### 3. Manual Activation (for future sessions)

To activate the environment for future use:

```cmd
activate.bat
```

### 4. Run the Application

```cmd
streamlit run main.py
```

The application will open in your default browser at `http://localhost:8501`

## Project Structure

```
ollama-streamlit-chat/
│
├── main.py                # Main Streamlit application
├── requirements.txt       # Python dependencies
├── create_venv.bat        # Virtual environment setup
├── activate.bat           # Environment activation script
└── README.md              # This file
```

## Usage Guide

### Model Selection

1. Choose from available models in the sidebar.
2. Models are automatically detected from your Ollama installation.
3. Switch between models at any time during conversation.

### Chat Settings

* **Temperature**: Controls response randomness (0.0 = deterministic, 2.0 = very creative).
* **Clear Chat**: Reset conversation history.

### Chat Interface

* Type messages in the input box at the bottom.
* Responses stream in real-time.
* Full conversation history is kept for reference.
* Supports copy/paste for code and text.

## Configuration

### Default Ollama Settings

* **Host**: `localhost`
* **Port**: `11434`
* **API Endpoint**: `http://localhost:11434`

### Customization

Edit the `OLLAMA_BASE_URL` variable in `main.py`:

```python
OLLAMA_BASE_URL = "http://your-host:your-port"
```

## Troubleshooting

### Common Issues

**❌ Cannot connect to Ollama**

* Ensure Ollama is running: `ollama serve`
* Check if port `11434` is accessible
* Verify Ollama installation

**❌ No models found**

* Pull at least one model: `ollama pull llama2`
* List available models: `ollama list`

**❌ Slow responses**

* Check system resources (RAM, CPU).
* Try smaller models (`phi`, `mistral`).
* Adjust temperature settings.

**❌ Python/pip errors**

* Ensure Python 3.7+ is installed.
* Update pip: `python -m pip install --upgrade pip`.
* Recreate the virtual environment if needed.

### Performance Tips

1. **Model Selection**: Use smaller models (`phi`, `mistral`) for faster results.
2. **System Resources**: Ensure at least 8GB RAM.
3. **Temperature**: Lower values (0.1–0.5) for faster, more focused responses.
4. **GPU Acceleration**: Ollama uses GPU if available.

## Dependencies

* **streamlit** (≥1.28.0) — Web application framework
* **requests** (≥2.31.0) — HTTP client for Ollama API

## Development

### Running in Development Mode

```cmd
# Activate environment
activate.bat

# Run with auto-reload
streamlit run main.py --server.runOnSave true
```

### Adding Features

The application is modular and easy to extend:

* Model management in `OllamaClient` class
* UI components in Streamlit
* Session state for persistence

## License

This project is licensed under the MIT License — see the LICENSE file for details.

## Acknowledgments

* [Ollama](https://ollama.ai/) — For providing the local LLM platform
* [Streamlit](https://streamlit.io/) — For the amazing web app framework
* Open source LLM community for the models

---
