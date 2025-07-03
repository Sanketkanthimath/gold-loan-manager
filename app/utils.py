from datetime import date

def calculate_interest(loan_amount: float, loan_date: date, rate: float = 0.01):
    months = (date.today().year - loan_date.year) * 12 + (date.today().month - loan_date.month)
    interest = loan_amount * rate * months
    return interest, months

def loan_age_color(months: int):
    if months >= 12:
        return "black"
    elif months >= 9:
        return "red"
    elif months >= 6:
        return "orange"
    else:
        return "none"