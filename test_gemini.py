from gemini_service import generate_banking_insights


result = generate_banking_insights(
    total_successful_amount=671461234,
    total_successful_transactions=58145,
    success_rate=96.91,
    active_customers=2999,
    total_loan_applications=8000,
    total_requested_loan_amount=500000000,
    total_approved_loan_amount=420000000,
    top_merchant_category="Groceries",
    top_payment_mode="UPI"
)

print(result)