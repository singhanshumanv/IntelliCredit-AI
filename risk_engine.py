def calculate_risk_score(data):

    score = 100

    revenue = data.get("revenue_by_year", {})
    profit = data.get("profit_by_year", {})
    debt = data.get("debt_by_year", {})
    risks = data.get("risks", [])

    # Debt risk
    if debt:
       latest_debt = list(debt.values())[-1]

    # convert dict/string to number safely
       if isinstance(latest_debt, dict):
         latest_debt = list(latest_debt.values())[0]

       try:
         latest_debt = float(latest_debt)
       except:
         latest_debt = 0

       if latest_debt > 200:
         score -= 20

    # Profit trend
    # Profit trend
    if profit:

      profits = []

      for v in profit.values():

         if isinstance(v, dict):
            v = list(v.values())[0]

         try:
            v = float(v)
         except:
            v = 0

         profits.append(v)

      if profits[-1] < profits[0]:
         score -= 15

    # Revenue growth
    if revenue:

      rev = []
      for v in revenue.values():
         if isinstance(v, dict):
             v = list(v.values())[0]

         try:
             v = float(v)
         except:
             v = 0

         rev.append(v)
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