def loan_decision(data, score):

    revenue = data.get("revenue_by_year", {})
    profit = data.get("profit_by_year", {})
    debt = data.get("debt_by_year", {})

    latest_revenue = list(revenue.values())[-1] if revenue else 0
    latest_profit = list(profit.values())[-1] if profit else 0
    latest_debt = list(debt.values())[-1] if debt else 0

    decision = "REJECT"
    amount = 0
    rate = 0

    if score >= 75:
        decision = "APPROVE"
        amount = latest_revenue * 0.20
        rate = 9.5

    elif score >= 50:
        decision = "APPROVE WITH CAUTION"
        amount = latest_revenue * 0.10
        rate = 11.5

    else:
        decision = "REJECT"
        amount = 0
        rate = 0

    return {
        "decision": decision,
        "loan_amount": amount,
        "interest_rate": rate
    }