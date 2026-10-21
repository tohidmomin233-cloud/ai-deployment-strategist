from deployment_planner.planner import build_plan, render_markdown, save_plan


def ask(prompt: str, default: str) -> str:
    answer = input(f"{prompt} [{default}]: ").strip()
    return answer or default


def main() -> None:
    print("\nAI-Assisted Deployment Strategist")
    print("Create a practical release plan for review.\n")
    project = ask("Project/application name", "Sample Web App")
    environment = ask("Environment (development/staging/production)", "staging").lower()
    deployment_type = ask("Application type (web application/api/data pipeline/mobile)", "web application").lower()
    strategy = ask("Release strategy (rolling/blue-green/canary/manual)", "rolling").lower()
    has_database = ask("Database changes included? (yes/no)", "no").lower() in {"yes", "y"}
    downtime = ask("Is planned downtime allowed? (yes/no)", "no").lower() in {"yes", "y"}

    plan = build_plan(project, environment, deployment_type, strategy, has_database, downtime)
    markdown = render_markdown(plan)
    output = save_plan(markdown, "deployment_plan.md")
    print("\n" + markdown)
    print(f"\nPlan saved to: {output}")


if __name__ == "__main__":
    main()
