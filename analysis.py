import pandas as pd
import numpy as np


# =========================================================
# 1. LOAD DATA
# =========================================================

transactions = pd.read_csv(
    r"C:\Users\Asus\OneDrive\Desktop\analytics-project\datasets\bank_transactions.csv"
)

customer = pd.read_csv(
    r"C:\Users\Asus\OneDrive\Desktop\analytics-project\datasets\customers_master.csv"
)

loan = pd.read_csv(
    r"C:\Users\Asus\OneDrive\Desktop\analytics-project\datasets\loan_info.csv"
)


# =========================================================
# 2. DATA TYPE CONVERSION
# =========================================================

transactions["transaction_date"] = pd.to_datetime(
    transactions["transaction_date"],
    errors="coerce"
)

customer["join_date"] = pd.to_datetime(
    customer["join_date"],
    errors="coerce"
)


# =========================================================
# 3. BASIC TRANSACTION ANALYSIS
# =========================================================

successful_transactions = transactions[
    transactions["transaction_status"] == "Success"
].copy()


total_successful_transactions_amount = (
    successful_transactions["amount"].sum()
)

total_successful_transactions_count = (
    successful_transactions["transaction_id"].nunique()
)

avg_successful_transactions_amount = (
    successful_transactions["amount"].mean()
)

total_transactions_count = transactions["transaction_id"].nunique()

percentage_success = (
    total_successful_transactions_count
    / total_transactions_count
) * 100


# =========================================================
# 4. DATE-BASED COLUMNS
# =========================================================

transactions["month_no"] = transactions["transaction_date"].dt.month

transactions["month"] = (
    transactions["transaction_date"].dt.month_name()
)

transactions["year"] = (
    transactions["transaction_date"].dt.year
)

transactions["day"] = (
    transactions["transaction_date"].dt.day_name()
)

transactions["day_no"] = (
    transactions["transaction_date"].dt.day_of_week
)


# Recreate successful transactions after adding date columns
success_tr = transactions[
    transactions["transaction_status"] == "Success"
].copy()


# =========================================================
# 5. MONTHLY TRANSACTION ANALYSIS
# =========================================================

year_month_wise_analysis = (
    success_tr
    .groupby(["year", "month_no", "month"])["amount"]
    .agg(
        total_amount="sum",
        average_amount="mean",
        transaction_count="count"
    )
    .sort_index()
)


# =========================================================
# 6. MERCHANT CATEGORY ANALYSIS
# =========================================================

merchant_category_analysis = (
    success_tr
    .groupby("merchant_category")["amount"]
    .agg(
        total_amount="sum",
        transaction_count="count"
    )
    .sort_values("total_amount", ascending=False)
)


# =========================================================
# 7. PAYMENT MODE ANALYSIS
# =========================================================

payment_analysis = (
    success_tr
    .groupby("payment_mode")["amount"]
    .agg(
        total_amount="sum",
        transaction_count="count",
        average_amount="mean"
    )
    .sort_values("total_amount", ascending=False)
)

payment_analysis["transaction_count_percentage"] = (
    payment_analysis["transaction_count"]
    / total_successful_transactions_count
) * 100


# =========================================================
# 8. CITY ANALYSIS
# =========================================================

city_analysis = (
    success_tr
    .groupby("city")["amount"]
    .agg(
        total_amount="sum",
        transaction_count="count"
    )
    .sort_values("total_amount", ascending=False)
    .head(10)
)


# =========================================================
# 9. ACCOUNT TYPE ANALYSIS
# =========================================================

account_type_analysis = (
    success_tr
    .groupby("account_type")["amount"]
    .agg(
        total_amount="sum",
        transaction_count="count",
        average_amount="mean"
    )
    .sort_values("total_amount", ascending=False)
)


# =========================================================
# 10. TRANSACTION STATUS BY PAYMENT MODE
# =========================================================

transactions_status_by_payment_mode = (
    transactions
    .pivot_table(
        index="payment_mode",
        columns="transaction_status",
        values="transaction_id",
        aggfunc="nunique",
        fill_value=0
    )
)


# =========================================================
# 11. MONTHLY TRANSACTION TREND BY STATUS
# =========================================================

monthly_transaction_trend_status = (
    transactions
    .pivot_table(
        index=["year", "month_no", "month"],
        columns="transaction_status",
        values="transaction_id",
        aggfunc="nunique",
        fill_value=0
    )
    .sort_index()
)


# =========================================================
# 12. CUSTOMER ACTIVITY ANALYSIS
# =========================================================

customer_activity_analysis = (
    success_tr
    .groupby(["customer_id", "customer_name"])["amount"]
    .agg(
        total_amount="sum",
        transaction_count="count"
    )
    .sort_values("total_amount", ascending=False)
)


no_of_active_customer = (
    success_tr["customer_id"].nunique()
)


# =========================================================
# 13. CITY-WISE ACTIVE CUSTOMER ANALYSIS
# =========================================================

city_wise_active_customer = (
    success_tr
    .groupby("city")
    .agg(
        active_customer=("customer_id", "nunique"),
        total_amount=("amount", "sum")
    )
    .sort_values("total_amount", ascending=False)
)


# =========================================================
# 14. ACCOUNT-WISE ACTIVE CUSTOMER ANALYSIS
# =========================================================

account_wise_active_cust_analysis = (
    success_tr
    .groupby("account_type")
    .agg(
        active_customer=("customer_id", "nunique"),
        total_amount=("amount", "sum"),
        average_amount=("amount", "mean")
    )
    .sort_values("total_amount", ascending=False)
)


# =========================================================
# 15. INCOME SEGMENT ANALYSIS
# =========================================================

joined_table = success_tr.merge(
    customer[["customer_id", "income_segment"]],
    on="customer_id",
    how="left"
)


income_segment_analysis = (
    joined_table
    .groupby("income_segment")["amount"]
    .agg(
        transaction_count="count",
        total_amount="sum",
        average_amount="mean"
    )
    .sort_values("total_amount", ascending=False)
)


income_segment_vs_customer_activity = (
    joined_table
    .groupby("income_segment")
    .agg(
        active_customer=("customer_id", "nunique"),
        total_amount=("amount", "sum"),
        average_transaction_amount=("amount", "mean")
    )
    .sort_values("total_amount", ascending=False)
)


# =========================================================
# 16. DAY-WISE ANALYSIS
# =========================================================

most_transactioned_day_of_week = (
    success_tr
    .groupby(["day_no", "day"])["amount"]
    .sum()
    .sort_index()
)


weekday_wise_analysis = (
    success_tr
    .groupby(["day_no", "day"])["amount"]
    .agg(
        transaction_count="count",
        total_amount="sum",
        average_amount="mean"
    )
    .sort_index()
)


# =========================================================
# 17. PAYMENT MODE AND TRANSACTION STATUS ANALYSIS
# =========================================================

temp1 = (
    transactions
    .pivot_table(
        index="payment_mode",
        columns="transaction_status",
        values="transaction_id",
        aggfunc="nunique",
        fill_value=0
    )
)

# Create missing columns if a status does not exist in the data
if "Failed" not in temp1.columns:
    temp1["Failed"] = 0

if "Success" not in temp1.columns:
    temp1["Success"] = 0


total_payment_mode_transactions = (
    temp1["Failed"] + temp1["Success"]
)

temp1["failure_rate"] = np.where(
    total_payment_mode_transactions > 0,
    (temp1["Failed"] / total_payment_mode_transactions) * 100,
    0
)


payment_vs_transaction_status_analysis = (
    temp1
    .sort_values("failure_rate", ascending=False)
)


# =========================================================
# 18. MONTH AND MERCHANT CATEGORY ANALYSIS
# =========================================================

month_merchant_category_analysis = (
    success_tr
    .groupby(
        ["month_no", "month", "merchant_category"]
    )["amount"]
    .sum()
    .sort_index()
)


# =========================================================
# 19. ACCOUNT TYPE AND PAYMENT MODE ANALYSIS
# =========================================================

account_type_and_payment_mode = (
    success_tr
    .groupby(["account_type", "payment_mode"])["amount"]
    .agg(
        total_amount="sum",
        transaction_count="count"
    )
    .sort_values("total_amount", ascending=False)
)


# =========================================================
# 20. RFM ANALYSIS
# =========================================================

# Latest successful transaction date for each customer
latest_transaction = (
    success_tr
    .groupby(
        ["customer_id", "customer_name"],
        as_index=False
    )
    .agg(
        latest_transaction_date=("transaction_date", "max")
    )
)


# Recency: number of days since the customer's latest transaction
latest_transaction["recency"] = (
    pd.Timestamp.today().normalize()
    - latest_transaction["latest_transaction_date"]
).dt.days


# Frequency: number of successful transactions
frequency = (
    success_tr
    .groupby(
        ["customer_id", "customer_name"],
        as_index=False
    )
    .agg(
        frequency=("transaction_id", "nunique")
    )
)


# Monetary: total successful transaction amount
monetary = (
    success_tr
    .groupby(
        ["customer_id", "customer_name"],
        as_index=False
    )
    .agg(
        monetary=("amount", "sum")
    )
)


# Combine RFM values
rfm = (
    latest_transaction
    .merge(
        frequency,
        on=["customer_id", "customer_name"],
        how="left"
    )
    .merge(
        monetary,
        on=["customer_id", "customer_name"],
        how="left"
    )
)


# Use ranking before qcut to avoid duplicate-value errors
rfm["R_score"] = (
    pd.qcut(
        rfm["recency"].rank(method="first"),
        5,
        labels=[5, 4, 3, 2, 1]
    )
    .astype(int)
)


rfm["F_score"] = (
    pd.qcut(
        rfm["frequency"].rank(method="first"),
        5,
        labels=[1, 2, 3, 4, 5]
    )
    .astype(int)
)


rfm["M_score"] = (
    pd.qcut(
        rfm["monetary"].rank(method="first"),
        5,
        labels=[1, 2, 3, 4, 5]
    )
    .astype(int)
)


# Combined RFM score
rfm["RFM_Score"] = (
    rfm["R_score"].astype(str)
    + rfm["F_score"].astype(str)
    + rfm["M_score"].astype(str)
)


# =========================================================
# 21. CUSTOMER SEGMENTATION
# =========================================================

rfm["segment"] = np.select(
    [
        (
            (rfm["R_score"] >= 4)
            & (rfm["F_score"] >= 4)
            & (rfm["M_score"] >= 4)
        ),

        (
            (rfm["R_score"] >= 3)
            & (rfm["F_score"] >= 4)
            & (rfm["M_score"] >= 3)
        ),

        (
            (rfm["R_score"] >= 4)
            & (rfm["F_score"] <= 3)
        ),

        (
            (rfm["R_score"] <= 2)
            & (rfm["F_score"] >= 3)
        ),

        (
            (rfm["R_score"] <= 2)
            & (rfm["F_score"] <= 2)
        )
    ],
    [
        "Champions",
        "Loyal Customers",
        "Potential Loyalists",
        "At Risk Customers",
        "Lost Customers"
    ],
    default="Regular Customers"
)


# =========================================================
# 22. SEGMENT ANALYSIS
# =========================================================

no_of_unique_customer = (
    rfm["customer_id"].nunique()
)


segment_analysis = (
    rfm
    .groupby("segment")
    .agg(
        no_of_customer=("customer_id", "nunique"),
        total_amount_per_segment=("monetary", "sum"),
        avg_amount_per_segment=("monetary", "mean")
    )
    .sort_values(
        "total_amount_per_segment",
        ascending=False
    )
)


segment_analysis["customer_contribution_per_segment"] = (
    segment_analysis["no_of_customer"]
    / no_of_unique_customer
) * 100


segment_analysis["amount_contribution_per_segment"] = (
    segment_analysis["total_amount_per_segment"]
    / segment_analysis["total_amount_per_segment"].sum()
) * 100


# =========================================================
# 23. HIGHEST VALUE CUSTOMERS
# =========================================================

highest_value_customer = (
    rfm
    .sort_values("monetary", ascending=False)
    .head(10)
    .reset_index(drop=True)
)


# =========================================================
# 24. BASIC LOAN ANALYSIS
# =========================================================

total_loan_applications = (
    loan["loan_id"].nunique()
)

total_requested_loan_amount = (
    loan["requested_loan_amount"].sum()
)

total_approved_loan_amount = (
    loan["approved_loan_amount"].sum()
)

loan_status_info = (
    loan["loan_status"].value_counts()
)


# =========================================================
# 25. LOAN CATEGORY ANALYSIS
# =========================================================

loan_category_analysis = (
    loan
    .groupby("loan_type")
    .agg(
        no_of_applications=("loan_id", "nunique"),
        total_requested_amount=(
            "requested_loan_amount",
            "sum"
        ),
        total_approved_amount=(
            "approved_loan_amount",
            "sum"
        )
    )
    .sort_values(
        "no_of_applications",
        ascending=False
    )
)


# =========================================================
# 26. CUSTOMER INCOME SEGMENT AND LOAN ANALYSIS
# =========================================================

merged_customer_loan = customer.merge(
    loan[
        [
            "customer_id",
            "loan_id",
            "requested_loan_amount",
            "approved_loan_amount"
        ]
    ],
    on="customer_id",
    how="left"
)


merged_customer_loan = merged_customer_loan[
    merged_customer_loan["loan_id"].notna()
]


income_segment_loan_analysis = (
    merged_customer_loan
    .groupby("income_segment")
    .agg(
        total_applications_incomewise=(
            "loan_id",
            "nunique"
        ),
        total_requested_amount_incomewise=(
            "requested_loan_amount",
            "sum"
        ),
        total_approved_amount_incomewise=(
            "approved_loan_amount",
            "sum"
        )
    )
    .sort_values(
        "total_applications_incomewise",
        ascending=False
    )
)


# =========================================================
# 27. EMPLOYMENT TYPE ANALYSIS
# =========================================================

employment_analysis = (
    loan
    .groupby("employment_type")
    .agg(
        no_of_applications=("loan_id", "nunique"),
        total_requested_amount=(
            "requested_loan_amount",
            "sum"
        ),
        total_approved_amount=(
            "approved_loan_amount",
            "sum"
        )
    )
    .sort_values(
        "no_of_applications",
        ascending=False
    )
)


# =========================================================
# 28. CREDIT SCORE CATEGORY ANALYSIS
# =========================================================

loan["credit_score_category"] = pd.cut(
    loan["credit_score"],
    bins=[0, 579, 669, 739, 900],
    labels=[
        "Poor",
        "Fair",
        "Good",
        "Excellent"
    ],
    include_lowest=True
)


credit_score_category_analysis = (
    loan
    .groupby(
        ["credit_score_category", "loan_status"],
        observed=False
    )["loan_id"]
    .nunique()
    .unstack(fill_value=0)
)


# =========================================================
# 29. CITY-WISE LOAN ANALYSIS
# =========================================================

city_loan_analysis = (
    loan
    .groupby("city")
    .agg(
        no_of_applications=("loan_id", "nunique"),
        total_requested_amount=(
            "requested_loan_amount",
            "sum"
        ),
        total_approved_amount=(
            "approved_loan_amount",
            "sum"
        )
    )
    .sort_values(
        "no_of_applications",
        ascending=False
    )
)


# =========================================================
# 30. LOAN STATUS ANALYSIS
# =========================================================

loan_status_analysis = (
    loan
    .groupby("loan_status")
    .agg(
        no_of_loans=("loan_id", "nunique"),
        total_requested_amount=(
            "requested_loan_amount",
            "sum"
        ),
        total_approved_amount=(
            "approved_loan_amount",
            "sum"
        )
    )
)


# =========================================================
# 31. EMI BURDEN ANALYSIS
# =========================================================

loan["EMI_Burden(%)"] = np.where(
    loan["monthly_income"] > 0,
    (
        loan["emi_amount"]
        / loan["monthly_income"]
    ) * 100,
    np.nan
)


loan["burden_type"] = np.select(
    [
        loan["EMI_Burden(%)"] < 20,
        loan["EMI_Burden(%)"].between(20, 35, inclusive="both"),
        loan["EMI_Burden(%)"].between(35.01, 50, inclusive="both")
    ],
    [
        "Low",
        "Moderate",
        "High"
    ],
    default="Very High"
)


# =========================================================
# 32. REPAYMENT ANALYSIS
# =========================================================

repayment_analysis = (
    loan
    .groupby("repayment_status")
    .agg(
        no_of_loans=("loan_id", "nunique"),
        total_loan_amount=(
            "approved_loan_amount",
            "sum"
        )
    )
    .sort_values(
        "no_of_loans",
        ascending=False
    )
)


# =========================================================
# 33. RFM AND LOAN ANALYSIS
# =========================================================

merge_rfm_loan = rfm.merge(
    loan,
    on="customer_id",
    how="left"
)


rfm_loan_analysis = (
    merge_rfm_loan
    .groupby("segment")
    .agg(
        no_of_customers=("customer_id", "nunique"),
        no_of_loan_applications=("loan_id", "nunique"),
        total_requested_amount=(
            "requested_loan_amount",
            "sum"
        ),
        total_approved_amount=(
            "approved_loan_amount",
            "sum"
        )
    )
    .sort_values(
        "no_of_loan_applications",
        ascending=False
    )
)


# =========================================================
# 34. OPTIONAL CHECKS
# =========================================================

print("Analysis completed successfully.")

print("\nTotal successful transaction amount:")
print(total_successful_transactions_amount)

print("\nTotal successful transactions:")
print(total_successful_transactions_count)

print("\nSuccess percentage:")
print(round(percentage_success, 2))

print("\nNumber of active customers:")
print(no_of_active_customer)

print("\nNumber of loan applications:")
print(total_loan_applications)

print("\nRFM segment analysis:")
print(segment_analysis)

print("\nLoan status analysis:")
print(loan_status_analysis)