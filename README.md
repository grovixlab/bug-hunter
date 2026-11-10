# Bug Hunter — Claude Code Skill

A reusable Claude Code skill for auditing vibe-coded and conventional software projects for functional bugs, UI glitches, security weaknesses, data-integrity risks, and regressions—then fixing verified, in-scope issues in priority order.

## Install

### Option A: Install in one repository

Copy the `.claude/skills/bug-hunter` directory from this repository into your project:

```text
your-project/
└── .claude/
    └── skills/
        └── bug-hunter/
            └── SKILL.md
```

Then open Claude Code in that project and invoke:

```text
/bug-hunter
```

### Option B: Install for your user (all projects)

Copy the skill directory to your user-level Claude skills directory:

```bash
mkdir -p ~/.claude/skills
cp -R .claude/skills/bug-hunter ~/.claude/skills/
```

Claude Code can then use `/bug-hunter` across projects.

## Example prompts

Audit and fix:

```text
/bug-hunter
Audit this codebase broadly. Verify findings, prioritize P0 through P4,
fix all safe in-scope issues in priority order, add regression tests,
and report the checks you actually ran.
```

Security-focused audit:

```text
/bug-hunter
Focus on authentication, authorization, data exposure, injection,
database policies, and security-sensitive business logic. Fix verified
issues safely and test the relevant flows.
```

Review only (no edits):

```text
/bug-hunter
Audit and prioritize issues, but do not modify any files. Give me the
findings and recommended fixes.
```

## Priority levels

- **P0 Critical** — catastrophic impact or severe exploitability
- **P1 High** — substantial security, data, payment, account, or core-flow impact
- **P2 Medium** — meaningful functional or reliability defects
- **P3 Low** — minor issues, edge cases, accessibility, or cosmetic defects
- **P4 Informational** — optional improvements and maintainability suggestions

## Safety

The skill is designed to preserve user changes and avoid destructive operations. It does not authorize production deployment, destructive database operations, external penetration testing, or handling secrets. Review Claude Code's proposed changes and verify them in your own environment before deploying.

## Repository contents

```text
.claude/skills/bug-hunter/SKILL.md   # Skill instructions
.github/workflows/ci.yml             # GitHub Actions CI workflow
scripts/validate.py                  # Repository & skill validation script
README.md                            # Installation and usage
LICENSE                              # MIT license
```

## Contributing

Issues and pull requests are welcome. Please include reproducible steps, expected behavior, actual behavior, and relevant test evidence when reporting a defect.

## Disclaimer

This skill is an aid to software review, not a guarantee of security, correctness, or production readiness. Automated and AI-assisted audits can miss vulnerabilities and can produce false positives. Use independent testing and professional security review for high-risk systems.
