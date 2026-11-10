#!/usr/bin/env python3
"""
Validation script for Bug Hunter Claude Code skill repository.
Checks file presence, skill YAML frontmatter, markdown formatting, and install simulation.
"""

import os
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

def check_file_exists(rel_path: str) -> Path:
    p = ROOT / rel_path
    if not p.is_file():
        raise AssertionError(f"Expected file does not exist: {rel_path}")
    if p.stat().st_size == 0:
        raise AssertionError(f"File is empty: {rel_path}")
    return p

def validate_skill():
    print("Checking skill definition...")
    skill_path = check_file_exists(".claude/skills/bug-hunter/SKILL.md")
    content = skill_path.read_text(encoding="utf-8")
    
    # Check frontmatter
    lines = content.splitlines()
    if not lines or lines[0].strip() != "---":
        raise AssertionError("SKILL.md must start with '---' YAML frontmatter delimiter.")
    
    end_idx = None
    for idx, line in enumerate(lines[1:], start=1):
        if line.strip() == "---":
            end_idx = idx
            break
            
    if end_idx is None:
        raise AssertionError("SKILL.md frontmatter is missing closing '---'.")
        
    frontmatter_text = "\n".join(lines[1:end_idx])
    
    name_match = re.search(r"^name:\s*([^\n]+)", frontmatter_text, re.MULTILINE)
    if not name_match or name_match.group(1).strip() != "bug-hunter":
        raise AssertionError(f"Expected skill name 'bug-hunter', got {name_match.group(1) if name_match else 'None'}")
        
    desc_match = re.search(r"^description:\s*([^\n]+)", frontmatter_text, re.MULTILINE)
    if not desc_match or len(desc_match.group(1).strip()) < 10:
        raise AssertionError("Skill description missing or too short.")
        
    # Check unclosed code blocks
    code_block_count = len(re.findall(r"^```", content, re.MULTILINE))
    if code_block_count % 2 != 0:
        raise AssertionError(f"Unclosed markdown code block in SKILL.md (found {code_block_count} backtick fences).")
        
    print("✓ SKILL.md frontmatter and structure are valid.")

def validate_readme():
    print("Checking README.md...")
    readme_path = check_file_exists("README.md")
    content = readme_path.read_text(encoding="utf-8")
    
    required_sections = [
        "# Bug Hunter",
        "## Install",
        "## Example prompts",
        "## Priority levels",
        "## Safety",
        "## Repository contents",
        "## Contributing",
        "## Disclaimer",
    ]
    for section in required_sections:
        if section not in content:
            raise AssertionError(f"README.md missing section: {section}")
            
    # Check unclosed code blocks
    code_block_count = len(re.findall(r"^```", content, re.MULTILINE))
    if code_block_count % 2 != 0:
        raise AssertionError(f"Unclosed markdown code block in README.md (found {code_block_count} backtick fences).")
        
    print("✓ README.md contains all required sections and valid code blocks.")

def validate_license():
    print("Checking LICENSE...")
    license_path = check_file_exists("LICENSE")
    content = license_path.read_text(encoding="utf-8")
    if "MIT License" not in content:
        raise AssertionError("LICENSE does not appear to be an MIT License.")
    print("✓ LICENSE is present and valid.")

def validate_installation_simulation():
    print("Testing simulated skill installation...")
    import tempfile
    import shutil
    
    src = ROOT / ".claude" / "skills" / "bug-hunter"
    
    with tempfile.TemporaryDirectory() as tmpdir:
        # Option A: project install
        dest_project = Path(tmpdir) / "project" / ".claude" / "skills" / "bug-hunter"
        dest_project.parent.mkdir(parents=True, exist_ok=True)
        shutil.copytree(src, dest_project)
        if not (dest_project / "SKILL.md").exists():
            raise AssertionError("Failed to simulate Option A install (project directory).")
            
        # Option B: user install
        dest_user = Path(tmpdir) / "user_home" / ".claude" / "skills" / "bug-hunter"
        dest_user.parent.mkdir(parents=True, exist_ok=True)
        shutil.copytree(src, dest_user)
        if not (dest_user / "SKILL.md").exists():
            raise AssertionError("Failed to simulate Option B install (user directory).")
            
    print("✓ Skill installation simulations succeeded.")

def main():
    print("Running Bug Hunter validation checks...")
    try:
        validate_license()
        validate_readme()
        validate_skill()
        validate_installation_simulation()
        print("\nAll validation checks passed successfully!")
    except AssertionError as e:
        print(f"\n❌ Validation failed: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
