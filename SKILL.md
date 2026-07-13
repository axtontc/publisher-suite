---
name: publisher-suite
description: >-
  The Master Publishing and Documentation CLI. Automatically generate premium documentation using a local LLM and publish your repository to GitHub in a single command.
license: MIT
metadata:
  version: v1.0.0
  publisher: Axton Carroll
---

# Publisher Suite

The Publisher Suite is the mathematically optimal CLI for deploying and documenting autonomous AI agent repositories.

## Modes of Operation

When the user asks you to package, document, or publish a repository, you have two primary tools:

### 1. Publisher Document
Scan a directory structure and its code snippets, and have a local LLM generate a premium `README.md` with Mermaid diagrams.
**Use when:** A repository needs documentation before publishing.
**Command:** `publisher document --path <directory>`

### 2. Publisher Publish
Initialize a Git repository (if needed), generate a `.gitignore`, commit changes, create a remote GitHub repository (Private by default), and push the code seamlessly.
**Use when:** A project is ready to be released or saved to GitHub.
**Command:** `publisher publish --path <directory>` (Use `--public` to make it a public repository).
