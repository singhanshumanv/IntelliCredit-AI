def explain_decision(data, score):

    explanation = []

    revenue = data.get("revenue_by_year", {})
    profit = data.get("profit_by_year", {})
    debt = data.get("debt_by_year", {})
    risks = data.get("risks", [])

    # revenue analysis
    if revenue:
        rev = list(revenue.values())
        if rev[-1] > rev[0]:
            explanation.append("✔ Revenue is growing")
        else:
            explanation.append("⚠ Revenue growth is weak")

    # profit analysis
    if profit:
        prof = list(profit.values())
        if prof[-1] >= prof[0]:
            explanation.append("✔ Profit trend positive")
        else:
            explanation.append("⚠ Profit declining")

    # debt analysis
    if debt:
        latest_debt = list(debt.values())[-1]
        if latest_debt > 200:
            explanation.append("⚠ Debt level is high")
        else:
            explanation.append("✔ Debt level manageable")

    # risk flags
    if risks:
        explanation.append(f"⚠ {len(risks)} risk factors detected")

    return explanation