from google import genai
import streamlit as st


# =========================================================
# GEMINI CLIENT
# =========================================================

client = genai.Client(
    api_key=st.secrets["GEMINI_API_KEY"]
)


# =========================================================
# GEMINI INSIGHT FUNCTION
# =========================================================

def generate_banking_insights(
    total_successful_amount,
    total_successful_transactions,
    success_rate,
    active_customers,
    total_loan_applications,
    total_requested_loan_amount,
    total_approved_loan_amount,
    top_merchant_category,
    top_payment_mode
):

    prompt = f"""
You are a banking data analyst.

Analyze the following banking dashboard metrics:

Total successful transaction amount:
{total_successful_amount}

Total successful transactions:
{total_successful_transactions}

Transaction success rate:
{success_rate:.2f}%

Active customers:
{active_customers}

Total loan applications:
{total_loan_applications}

Total requested loan amount:
{total_requested_loan_amount}

Total approved loan amount:
{total_approved_loan_amount}

Top merchant category:
{top_merchant_category}

Most-used payment mode:
{top_payment_mode}

Generate a concise business analysis with exactly these sections:

1. Transaction Performance
2. Customer Insights
3. Loan Insights
4. Business Recommendations

Rules:
- Use only the provided metrics.
- Do not invent additional numbers.
- Keep the explanation simple and professional.
- Give practical recommendations.
- Use bullet points.
"""


    response = client.models.generate_content(
    model="gemini-3.6-flash",
    contents=prompt
    )

    return response.text