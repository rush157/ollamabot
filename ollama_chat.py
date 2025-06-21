import streamlit as st
import requests
import json
from typing import Dict, List, Generator
import time  # noqa: F401

# Configure Streamlit page
st.set_page_config(
    page_title="Ollama Chat",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Ollama API configuration
OLLAMA_BASE_URL = "http://localhost:11434"

class OllamaClient:
    def __init__(self, base_url: str = OLLAMA_BASE_URL):
        self.base_url = base_url
    
    def get_models(self) -> List[str]:
        """Fetch available models from Ollama"""
        try:
            response = requests.get(f"{self.base_url}/api/tags", timeout=5)
            if response.status_code == 200:
                models = response.json().get("models", [])
                return [model["name"] for model in models]
            return []
        except requests.exceptions.RequestException:
            return []
    
    def check_connection(self) -> bool:
        """Check if Ollama is running"""
        try:
            response = requests.get(f"{self.base_url}/api/tags", timeout=5)
            return response.status_code == 200
        except requests.exceptions.RequestException:
            return False
    
    def chat_stream(self, model: str, messages: List[Dict], temperature: float = 0.7) -> Generator[str, None, None]:
        """Stream chat responses from Ollama"""
        try:
            payload = {
                "model": model,
                "messages": messages,
                "stream": True,
                "options": {
                    "temperature": temperature
                }
            }
            
            response = requests.post(
                f"{self.base_url}/api/chat",
                json=payload,
                stream=True,
                timeout=30
            )
            
            if response.status_code == 200:
                for line in response.iter_lines():
                    if line:
                        try:
                            data = json.loads(line.decode('utf-8'))
                            if 'message' in data and 'content' in data['message']:
                                yield data['message']['content']
                        except json.JSONDecodeError:
                            continue
            else:
                yield f"Error: HTTP {response.status_code}"
                
        except requests.exceptions.RequestException as e:
            yield f"Connection error: {str(e)}"

def initialize_session_state():
    """Initialize session state variables"""
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "selected_model" not in st.session_state:
        st.session_state.selected_model = None
    if "ollama_client" not in st.session_state:
        st.session_state.ollama_client = OllamaClient()

def main():
    initialize_session_state()
    
    # Title and description
    st.title("🤖 Ollama Chat Interface")
    st.markdown("Chat with local LLMs using Ollama")
    
    # Sidebar configuration
    with st.sidebar:
        st.header("⚙️ Configuration")
        
        # Connection status
        if st.session_state.ollama_client.check_connection():
            st.success("✅ Connected to Ollama")
        else:
            st.error("❌ Cannot connect to Ollama")
            st.info("Make sure Ollama is running on localhost:11434")
            st.stop()
        
        # Model selection
        st.subheader("Model Selection")
        available_models = st.session_state.ollama_client.get_models()
        
        if not available_models:
            st.warning("No models found. Please pull a model using: `ollama pull <model-name>`")
            st.info("Popular models: llama2, mistral, codellama, phi, neural-chat")
            st.stop()
        
        selected_model = st.selectbox(
            "Choose a model:",
            available_models,
            index=0 if available_models else None
        )
        
        if selected_model != st.session_state.selected_model:
            st.session_state.selected_model = selected_model
            st.rerun()
        
        # Chat settings
        st.subheader("Chat Settings")
        temperature = st.slider(
            "Temperature",
            min_value=0.0,
            max_value=2.0,
            value=0.7,
            step=0.1,
            help="Controls randomness in responses"
        )
        
        # Clear chat button
        if st.button("🗑️ Clear Chat", use_container_width=True):
            st.session_state.messages = []
            st.rerun()
        
        # Model info
        if selected_model:
            st.subheader("Current Model")
            st.info(f"**{selected_model}**")
    
    # Main chat interface
    if not st.session_state.selected_model:
        st.info("Please select a model from the sidebar to start chatting.")
        return
    
    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # Chat input
    if prompt := st.chat_input("Type your message here..."):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # Display user message
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Generate and display assistant response
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            full_response = ""
            
            # Prepare messages for API call
            api_messages = [
                {"role": msg["role"], "content": msg["content"]} 
                for msg in st.session_state.messages
            ]
            
            # Stream the response
            try:
                for chunk in st.session_state.ollama_client.chat_stream(
                    st.session_state.selected_model, 
                    api_messages, 
                    temperature
                ):
                    full_response += chunk
                    message_placeholder.markdown(full_response + "▌")
                
                message_placeholder.markdown(full_response)
                
            except Exception as e:
                error_message = f"Error generating response: {str(e)}"
                message_placeholder.error(error_message)
                full_response = error_message
        
        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": full_response})

if __name__ == "__main__":
    main()