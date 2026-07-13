import argparse
import sys
import os

def main():
    parser = argparse.ArgumentParser(description="Publisher Suite: The mathematically optimal CLI for Autonomous Publication.")
    subparsers = parser.add_subparsers(dest="command", required=True)
    
    # Publish Command (from github-publisher)
    publish_parser = subparsers.add_parser("publish", help="Initialize, commit, and push a directory to GitHub")
    publish_parser.add_argument("--path", type=str, required=True, help="Directory to publish")
    publish_parser.add_argument("--public", action="store_true", help="Make repository public")
    
    # Document Command (from auto-github-repo)
    document_parser = subparsers.add_parser("document", help="Autonomously generate a README and ledger using a local LLM")
    document_parser.add_argument("--path", type=str, required=True, help="Project root directory")
    
    args = parser.parse_args()
    
    if args.command == "publish":
        from publisher.core.publish_core import run_publish
        run_publish(args.path, args.public)
    elif args.command == "document":
        from publisher.core.document_core import run_document
        run_document(args.path)
    else:
        parser.print_help()
        sys.exit(1)

if __name__ == "__main__":
    main()
