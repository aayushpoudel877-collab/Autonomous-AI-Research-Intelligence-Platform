from nexus.research.planner import ResearchPlanner


def test_planner_produces_bounded_plan():
    plan = ResearchPlanner().plan("What is NEXUS and how does it work?", max_subquestions=3)
    assert 1 <= len(plan.subquestions) <= 3
    assert plan.question.startswith("What is NEXUS")
