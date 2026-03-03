from app.rules import calculate_risk

def test_high_risk_many_tickets():
    customer = {
        "contract_type": "One year",
        "monthly_charge_change": 0
    }

    tickets = [{"date": "2026-02-01", "category": "billing"}] * 6

    assert calculate_risk(customer, tickets) == "HIGH"


def test_low_risk():
    customer = {
        "contract_type": "One year",
        "monthly_charge_change": 0
    }

    tickets = []

    assert calculate_risk(customer, tickets) == "LOW"
