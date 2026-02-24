def calculate_final_score(analysis):

    intent_map = {"low": 3, "medium": 6, "high": 9}
    budget_map = {"low": 3, "moderate": 6, "high": 9}
    timeline_map = {"immediate": 9, "soon": 7, "later": 4, "unclear": 3}
    faq_map = {"low": 3, "medium": 6, "high": 9}

    intent_score = intent_map.get(analysis["intent_level"], 0)
    budget_score = budget_map.get(analysis["budget_fit"], 0)
    timeline_score = timeline_map.get(analysis["timeline_readiness"], 0)
    faq_score = faq_map.get(analysis["faq_engagement_level"], 0)
    overall = analysis["overall_interest_score"]

    final_score = (
        intent_score * 0.3 +
        budget_score * 0.2 +
        timeline_score * 0.2 +
        faq_score * 0.1 +
        overall * 0.2
    )

    return round(final_score, 2)