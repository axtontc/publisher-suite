<div align="center">
  
# 🚀 Publisher Suite

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://python.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

The mathematically optimal CLI for deploying and documenting autonomous AI agent repositories. Automatically generate premium documentation and publish your repository to GitHub in a single command.

[Installation](#installation) •
[Usage](#usage) •
[Agent Integration](#agent-integration)

</div>

---

## 🛑 The Problem

Publishing a new repository manually is tedious. It requires:
- Initializing a Git repository.
- Writing a `.gitignore` and `README.md`.
- Staging and committing changes.
- Creating a remote GitHub repository via the website or gh CLI.
- Pushing the code.

For an autonomous AI agent, this process is even harder to orchestrate across multiple tools.

## 💡 The Solution

**Publisher Suite** wraps documentation auto-generation (via local LLMs) and full GitHub publication into a streamlined, standalone CLI.

---

## 🚀 Installation

Install directly via `pip` or use `uv`.

```bash
git clone https://github.com/axtontc/publisher-suite
cd publisher-suite
pip install .
```

For the documentation feature, ensure you have a local Ollama instance running. Models are dynamically pulled from `~/.gemini/config/models.json`.
For the publishing feature, ensure you have a `GITHUB_TOKEN` environment variable set, or saved in your local `credentials.json`.

---

## 💻 Usage (CLI)

### 1. Document
Autonomously scan your project and generate a premium `README.md`:
```bash
publisher document --path ./my_project
```

### 2. Publish
Initialize, commit, create the remote repository, and push to GitHub:
```bash
publisher publish --path ./my_project
```
Add the `--public` flag to make the repository public.

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
