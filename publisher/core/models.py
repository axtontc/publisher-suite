import os
import json

def get_model(model_type="llm"):
    config_path = r"C:\Users\axton\.gemini\config\models.json"
    if os.path.exists(config_path):
        try:
            with open(config_path, "r", encoding="utf-16") as f:
                data = json.load(f)
                return data.get(model_type, "qwen2.5-coder:7b" if model_type == "llm" else "nomic-embed-text")
        except:
            try:
                with open(config_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    return data.get(model_type, "qwen2.5-coder:7b" if model_type == "llm" else "nomic-embed-text")
            except: pass
            
    if model_type == "llm":
        return os.getenv("OLLAMA_LLM", "qwen2.5-coder:7b")
    else:
        return os.getenv("OLLAMA_EMBEDDING", "nomic-embed-text")
