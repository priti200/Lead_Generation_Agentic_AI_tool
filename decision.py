def decide_crm_category(score):
    """
    Maps AI score (0-10) to CRM storage category.
    """

    if score >= 8:
        return "Interested"

    elif score >= 6:
        return "Needs More Clarification"

    elif score >= 4:
        return "Contact in Future"

    else:
        return "Not Interested"
