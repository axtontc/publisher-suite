import os
import sys
import subprocess
import json
import urllib.request
import urllib.error

def run_cmd(args, cwd=None):
    res = subprocess.run(args, capture_output=True, text=True, cwd=cwd)
    return res.stdout.strip(), res.stderr.strip(), res.returncode

def get_github_token():
    token = os.getenv("GITHUB_TOKEN")
    if token: return token
    config_path = r"C:\Users\axton\.gemini\config\credentials.json"
    if os.path.exists(config_path):
        try:
            with open(config_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                token = data.get("github_token")
                if token: return token
        except Exception: pass
    return None

def fetch_username(token):
    req = urllib.request.Request(
        "https://api.github.com/user",
        headers={"Authorization": f"token {token}", "Accept": "application/vnd.github.v3+json", "User-Agent": "Antigravity-Publisher"}
    )
    try:
        with urllib.request.urlopen(req) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            return data.get("login")
    except Exception as e:
        print(f"Failed to query username: {e}")
        sys.exit(1)

def create_remote_repo(token, name, description, is_private=True):
    payload = json.dumps({"name": name, "description": description or "Published autonomously", "private": is_private, "auto_init": False}).encode("utf-8")
    req = urllib.request.Request(
        "https://api.github.com/user/repos", data=payload, method="POST",
        headers={"Authorization": f"token {token}", "Content-Type": "application/json", "Accept": "application/vnd.github.v3+json", "User-Agent": "Antigravity-Publisher"}
    )
    try:
        with urllib.request.urlopen(req) as resp:
            print(f"Remote repository '{name}' created successfully on GitHub!")
            return True
    except urllib.error.HTTPError as e:
        err_msg = e.read().decode("utf-8")
        if "already exists" in err_msg or e.code == 422:
            print(f"Remote repository '{name}' already exists. Proceeding to push changes.")
            return True
        else:
            print(f"Error creating GitHub repository: {err_msg}")
            sys.exit(1)
    except Exception as e:
        print(f"Failed to create repository: {e}")
        sys.exit(1)

def run_publish(path, is_public):
    project_path = os.path.abspath(path)
    if not os.path.isdir(project_path):
        print(f"Error: Target path '{project_path}' is not a directory.")
        sys.exit(1)
        
    repo_name = os.path.basename(project_path)
    print(f"Target repository: {repo_name} at {project_path}")
    
    token = get_github_token()
    if not token:
        print("Error: GITHUB_TOKEN not found in environment variables or credentials config.")
        sys.exit(1)
        
    username = fetch_username(token)
    print(f"Authenticated as GitHub user: {username}")
    
    git_dir = os.path.join(project_path, ".git")
    if not os.path.exists(git_dir):
        print("Initializing Git repository locally...")
        run_cmd(["git", "init"], cwd=project_path)
            
    gitignore_path = os.path.join(project_path, ".gitignore")
    if not os.path.exists(gitignore_path):
        with open(gitignore_path, "w", encoding="utf-8") as f:
            f.write("*.pyc\n__pycache__/\n.venv/\nvenv/\n.env\n.agents/\n")
            
    description = ""
    readme_path = os.path.join(project_path, "README.md")
    if os.path.exists(readme_path):
        try:
            with open(readme_path, "r", encoding="utf-8") as f:
                first_lines = [f.readline() for _ in range(5)]
                description = " ".join([l.strip() for l in first_lines if l.strip() and not l.startswith("#")])[:100]
        except Exception: pass
    else:
        with open(readme_path, "w", encoding="utf-8") as f:
            f.write(f"# {repo_name}\n\nPublished autonomously.\n")
            
    print("Staging and committing files...")
    run_cmd(["git", "add", "."], cwd=project_path)
    run_cmd(["git", "commit", "-m", "Initial commit"], cwd=project_path)
    run_cmd(["git", "branch", "-M", "main"], cwd=project_path)
    
    create_remote_repo(token, repo_name, description, not is_public)
    
    remote_url = f"https://x-access-token:{token}@github.com/{username}/{repo_name}.git"
    run_cmd(["git", "remote", "remove", "origin"], cwd=project_path)
    stdout, stderr, code = run_cmd(["git", "remote", "add", "origin", remote_url], cwd=project_path)
    if code != 0:
        print(f"Error configuring remote origin: {stderr}")
        sys.exit(1)
        
    print("Pushing branch 'main' to GitHub...")
    stdout, stderr, code = run_cmd(["git", "push", "-u", "origin", "main", "--force"], cwd=project_path)
    if code != 0:
        print(f"Push failed: {stderr}")
        sys.exit(1)
        
    print(f"SUCCESS! Repository successfully pushed to: https://github.com/{username}/{repo_name}")
