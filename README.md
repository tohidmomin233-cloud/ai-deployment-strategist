# AI-Assisted Deployment Strategist

A lightweight Python command-line tool that helps a team prepare for a software release. It creates a deployment checklist, highlights common risks, and generates a rollback plan based on project details.

> Portfolio demo: this tool uses rule-based recommendations, not a live AI model or production deployment system.

## Features
- Generates a deployment checklist based on release type and environment.
- Highlights common release risks.
- Produces a rollback plan.
- Exports the plan as Markdown.
- Includes sample output and automated tests.

## Requirements
- Python 3.10+
- No third-party packages required

## Run
```bash
python main.py
```
Answer the prompts. The tool saves the result as `deployment_plan.md`.

## Run tests
```bash
python -m unittest discover -s tests -v
```

## Project structure
```text
ai-deployment-strategist/
├── main.py
├── deployment_planner/
│   ├── __init__.py
│   └── planner.py
├── tests/
│   └── test_planner.py
├── examples/
│   └── sample_deployment_plan.md
├── .gitignore
└── README.md
```

## Responsible use
This is a portfolio/demo tool. It does not connect to cloud infrastructure, deploy code, inspect a real system, or replace an engineer's review. Validate all suggestions against the actual system and approved release procedures.

## Future improvements
- Add a web UI.
- Integrate an approved language-model API for optional AI-generated suggestions.
- Add organization-specific templates.
- Integrate CI/CD status checks with suitable permissions.
