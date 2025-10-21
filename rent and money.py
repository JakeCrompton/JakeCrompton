def calculate_savings(income_per_term, rent_per_term, weekly_spending, weeks_per_term=14, terms_per_year=3, years=3):
    # Money left after rent
    after_rent = income_per_term - rent_per_term
    
    # Spending per term
    spending_per_term = weekly_spending * weeks_per_term
    
    # Savings per term
    savings_per_term = after_rent - spending_per_term
    
    # Savings per year
    savings_per_year = savings_per_term * terms_per_year
    
    # Savings after all years
    total_savings = savings_per_year * years
    
    return {
        "savings_per_term": round(savings_per_term, 2),
        "savings_per_year": round(savings_per_year, 2),
        "total_savings": round(total_savings, 2)
    }

income_per_term = 3516.81
rent_per_term = 1923.14
weekly_spending = 60

results = calculate_savings(income_per_term, rent_per_term, weekly_spending)

print("Savings per term: £", results["savings_per_term"])
print("Savings per year: £", results["savings_per_year"])
print("Total savings after 3 years: £", results["total_savings"])
