import os
import requests
from publisher.core.models import get_model


def analyze_directory(path):
    structure = []
    content = ""
    for root, dirs, files in os.walk(path):
        if ".git" in root or "__pycache__" in root or ".venv" in root:
            continue
        structure.append(root.replace(path, ""))
        for f in files:
            if f.endswith(".py") or f.endswith(".md"):
                file_path = os.path.join(root, f)
                structure.append(f"  - {f}")
                try:
                    with open(file_path, "r", encoding="utf-8") as file:
                        if len(content) < 8000:
                            content += f"--- {f} ---\n{file.read()[:1000]}\n"
                except: pass
    return "\n".join(structure), content

def run_document(path):
    print(f"[*] Documenting {path} via LLM...")
    structure, snippets = analyze_directory(path)
    
    prompt = f"""You are a senior technical writer. Create a premium README.md for this project.
    Output only the raw markdown. Use Mermaid diagrams if applicable.

    Directory Structure:
    {structure}

    Code Snippets:
    {snippets}
    """
    
    try:
        res = requests.post("http://localhost:11434/api/generate", json={
            "model": get_model("llm"),
            "prompt": prompt,
            "stream": False
        }, timeout=60)
        markdown = res.json().get("response", "").replace("```markdown", "").replace("```", "").strip()
        
        readme_path = os.path.join(path, "README.md")
        with open(readme_path, "w", encoding="utf-8") as f:
            f.write(markdown)
        print(f"[*] Successfully generated {readme_path}")
    except Exception as e:
        print(f"[!] Documentation generation failed: {e}")
