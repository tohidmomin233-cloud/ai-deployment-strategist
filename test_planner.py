import unittest
from deployment_planner.planner import build_plan, render_markdown


class DeploymentPlannerTests(unittest.TestCase):
    def test_production_plan_contains_approval(self):
        plan = build_plan("Payments API", environment="production")
        self.assertEqual(plan["environment"], "production")
        self.assertTrue(any("production release approval" in item.lower() for item in plan["checklist"]))

    def test_database_changes_add_migration_risk(self):
        plan = build_plan("Reporting Service", has_database_changes=True)
        self.assertTrue(any("migration" in risk.lower() for risk, _ in plan["risks"]))
        self.assertTrue(any("database" in item.lower() for item in plan["rollback"]))

    def test_invalid_values_fall_back_safely(self):
        plan = build_plan("Demo", environment="live", strategy="magic")
        self.assertEqual(plan["environment"], "staging")
        self.assertEqual(plan["strategy"], "manual")

    def test_markdown_has_checklist_and_rollback(self):
        output = render_markdown(build_plan("Demo"))
        self.assertIn("Pre-deployment checklist", output)
        self.assertIn("Rollback plan", output)
        self.assertIn("- [ ]", output)


if __name__ == "__main__":
    unittest.main()
