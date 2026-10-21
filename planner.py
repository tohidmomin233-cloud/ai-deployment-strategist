from datetime import date
from pathlib import Path
from typing import Dict, List

VALID_ENVIRONMENTS = {"development", "staging", "production"}
VALID_STRATEGIES = {"rolling", "blue-green", "canary", "manual"}


def build_plan(project: str, environment: str = "staging",
               deployment_type: str = "web application", strategy: str = "rolling",
               has_database_changes: bool = False, downtime_allowed: bool = False) -> Dict[str, object]:
    env = environment.lower().strip()
    release_strategy = strategy.lower().strip()
    if env not in VALID_ENVIRONMENTS:
        env = "staging"
    if release_strategy not in VALID_STRATEGIES:
        release_strategy = "manual"

    checklist: List[str] = [
        "Confirm release scope, owner, communication channel, and approval.",
        "Verify the build passed automated tests and code review.",
        "Confirm configuration and secrets are supplied through approved secure systems.",
        "Check monitoring, alerting, and log access before release.",
        "Record the current version and verify a known-good rollback artifact exists.",
        "Notify stakeholders of the deployment window and success criteria.",
    ]
    if env == "production":
        checklist += [
            "Obtain production release approval and confirm on-call coverage.",
            "Verify backup/recovery readiness and define a go/no-go decision owner.",
            "Deploy during the approved window and monitor key service-level indicators.",
        ]
    else:
        checklist += [
            "Validate the release in the target environment before promoting it further.",
            "Capture test results and record known limitations.",
        ]

    kind = deployment_type.lower()
    if "api" in kind:
        checklist += ["Check API compatibility, authentication, rate limits, and contract tests.",
                       "Confirm health endpoints and backward compatibility for clients."]
    elif "data" in kind:
        checklist += ["Validate input schema, data quality checks, and pipeline idempotency.",
                       "Confirm recovery/reprocessing steps and expected data freshness."]
    elif "mobile" in kind:
        checklist += ["Verify store submission status, supported versions, and staged rollout settings.",
                       "Prepare crash monitoring and a user-support communication plan."]
    else:
        checklist += ["Run smoke tests for core user journeys and verify routing.",
                       "Check client compatibility and application health endpoints."]

    if has_database_changes:
        checklist += [
            "Review migration scripts and test them against representative data.",
            "Prefer backward-compatible migrations; verify backup and restore steps.",
            "Document a forward-fix option; do not assume database rollback is safe.",
        ]
    if not downtime_allowed:
        checklist.append("Confirm the release strategy minimizes downtime and define traffic-shift steps.")
    else:
        checklist.append("Communicate the approved downtime window and prepare maintenance messaging.")

    risks = [
        ("Unhealthy release", "Use smoke tests and health checks; stop promotion if checks fail."),
        ("Configuration mismatch", "Validate environment configuration and required variables."),
        ("Insufficient observability", "Confirm dashboards, logs, and alert routing before starting."),
    ]
    if env == "production":
        risks.append(("Customer impact", "Use staged traffic rollout where possible and keep an incident owner available."))
    if has_database_changes:
        risks.append(("Data migration issue", "Test migration and restore procedures; prepare a forward-fix plan."))
    if release_strategy == "canary":
        risks.append(("Canary metrics are inconclusive", "Define success thresholds and observation duration before expanding traffic."))
    elif release_strategy == "blue-green":
        risks.append(("Environment drift", "Keep environments aligned and test routing switch-back."))
    elif release_strategy == "rolling":
        risks.append(("Mixed application versions", "Ensure adjacent versions remain compatible during rollout."))

    rollback = [
        "Declare rollback if agreed health checks fail, error rates rise materially, or critical journeys break.",
        "Pause rollout and notify the release owner and incident channel.",
        "Route traffic back to the last known-good version or restore the previous artifact.",
        "Verify service health, core user journeys, logs, and key metrics after rollback.",
        "Record the timeline, impact, decision, and follow-up actions.",
    ]
    if has_database_changes:
        rollback.insert(3, "Follow the reviewed database recovery plan; avoid untested destructive reverse migrations.")
    if release_strategy == "blue-green":
        rollback[2] = "Switch traffic back to the previous healthy environment and verify routing."
    elif release_strategy == "canary":
        rollback[2] = "Stop canary expansion and shift traffic back to the stable version."

    return {
        "project": project.strip() or "Unnamed Project",
        "date": date.today().isoformat(),
        "environment": env,
        "deployment_type": deployment_type,
        "strategy": release_strategy,
        "checklist": checklist,
        "risks": risks,
        "rollback": rollback,
        "note": "Demo recommendations only; review with the responsible engineering and operations teams.",
    }


def render_markdown(plan: Dict[str, object]) -> str:
    lines = [
        f"# Deployment Plan: {plan['project']}", "",
        f"- **Date:** {plan['date']}",
        f"- **Environment:** {plan['environment']}",
        f"- **Application type:** {plan['deployment_type']}",
        f"- **Release strategy:** {plan['strategy']}", "",
        "## Pre-deployment checklist",
    ]
    lines += [f"- [ ] {item}" for item in plan["checklist"]]
    lines += ["", "## Risk register", "", "| Risk | Mitigation |", "|---|---|"]
    lines += [f"| {risk} | {mitigation} |" for risk, mitigation in plan["risks"]]
    lines += ["", "## Rollback plan"]
    lines += [f"{i}. {item}" for i, item in enumerate(plan["rollback"], start=1)]
    lines += ["", f"> **Note:** {plan['note']}", ""]
    return "\n".join(lines)


def save_plan(markdown: str, filename: str = "deployment_plan.md") -> str:
    path = Path(filename)
    path.write_text(markdown, encoding="utf-8")
    return str(path)
