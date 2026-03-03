from datetime import datetime

def calculate_risk(customer, tickets):
    ticket_count_30d = 0

    for t in tickets:
        ticket_date = datetime.strptime(t["date"], "%Y-%m-%d")
        days_diff = (datetime.now() - ticket_date).days
        if days_diff <= 30:
            ticket_count_30d += 1

    # Rule 1: >5 tickets in 30 days
    if ticket_count_30d > 5:
        return "HIGH"

    # Rule 2: Monthly charge increased + 3 tickets
    if customer["monthly_charge_change"] > 0 and ticket_count_30d >= 3:
        return "MEDIUM"

    # Rule 3: Month-to-Month + complaint
    if customer["contract_type"] == "Month-to-Month":
        for t in tickets:
            if t["category"] == "complaint":
                return "HIGH"

    return "LOW"
