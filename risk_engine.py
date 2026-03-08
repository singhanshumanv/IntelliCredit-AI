def calculate_risk_score(data):

    score = 100

    revenue = data.get("revenue_by_year", {})
    profit = data.get("profit_by_year", {})
    debt = data.get("debt_by_year", {})
    risks = data.get("risks", [])

    # Debt risk
    if debt:
        latest_debt = list(debt.values())[-1]
        if latest_debt > 200:
            score -= 20

    # Profit trend
    if profit:
        profits = list(profit.values())
        if profits[-1] < profits[0]:
            score -= 15

    # Revenue growth
    if revenue:
        rev = list(revenue.values())
        if rev[-1] <= rev[0]:
            score -= 10

    # Legal risks
    score -= len(risks) * 10

    score = max(score, 0)

    return score





def risk_category(score):

    if score >= 75:
        return "Low Risk"

    elif score >= 45:
        return "Medium Risk"

    else:
        return "High Risk"