
import streamlit as st
import plotly.express as px
import analysis
from gemini_service import generate_banking_insights


# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="Banking Analytics Dashboard",
    page_icon="🏦",
    layout="wide"
)


# =========================================================
# SESSION STATE
# =========================================================

if "page" not in st.session_state:
    st.session_state.page = "Overview"

if "ai_insights" not in st.session_state:
    st.session_state.ai_insights = None


# =========================================================
# HELPER FUNCTIONS
# =========================================================

def format_amount(amount):
    """
    Convert large amounts into readable formats.

    Example:
    671461234 -> ₹671.46M
    2350000000 -> ₹2.35B
    850000 -> ₹850.00K
    """

    if amount >= 1_000_000_000:
        return f"₹{amount / 1_000_000_000:.2f}B"

    elif amount >= 1_000_000:
        return f"₹{amount / 1_000_000:.2f}M"

    elif amount >= 1_000:
        return f"₹{amount / 1_000:.2f}K"

    else:
        return f"₹{amount:,.0f}"


def change_page(page_name):
    st.session_state.page = page_name


def generate_ai_insights():
    """
    Generate banking insights using Gemini API.
    """

    try:
        with st.spinner("Gemini is analyzing your banking data..."):

            insights = generate_banking_insights(
                total_successful_amount=(
                    analysis.total_successful_transactions_amount
                ),

                total_successful_transactions=(
                    analysis.total_successful_transactions_count
                ),

                success_rate=analysis.percentage_success,

                active_customers=analysis.no_of_active_customer,

                total_loan_applications=(
                    analysis.total_loan_applications
                ),

                total_requested_loan_amount=(
                    analysis.total_requested_loan_amount
                ),

                total_approved_loan_amount=(
                    analysis.total_approved_loan_amount
                ),

                top_merchant_category=(
                    analysis.merchant_category_analysis
                    .reset_index()
                    .iloc[0]["merchant_category"]
                ),

                top_payment_mode=(
                    analysis.payment_analysis
                    .reset_index()
                    .iloc[0]["payment_mode"]
                )
            )

            st.session_state.ai_insights = insights

    except Exception as error:
        st.error("Unable to generate AI insights.")
        st.exception(error)


# =========================================================
# CUSTOM CSS
# =========================================================

st.markdown(
    """
    <style>

    /* Main dashboard title */
    .main-title {
        font-size: 32px;
        font-weight: 700;
        color: #FFFFFF !important;
        margin-bottom: 5px;
    }

    /* Subtitle */
    .sub-title {
        font-size: 15px;
        color: #CBD5E1 !important;
        margin-bottom: 20px;
    }

    /* Sidebar background */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0F172A, #1E293B);
        padding-top: 25px;
    }

    /* Sidebar text */
    [data-testid="stSidebar"] * {
        color: #FFFFFF;
    }

    .sidebar-title {
        font-size: 25px;
        font-weight: 700;
        color: #FFFFFF !important;
        margin-bottom: 5px;
    }

    .sidebar-subtitle {
        font-size: 13px;
        color: #CBD5E1 !important;
        margin-bottom: 25px;
    }

    .sidebar-section {
        font-size: 12px;
        font-weight: 600;
        color: #94A3B8 !important;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-top: 15px;
        margin-bottom: 10px;
    }

    /* Sidebar navigation buttons */
    [data-testid="stSidebar"] .stButton > button {
        width: 100%;
        min-height: 45px;
        border: 1px solid transparent;
        border-radius: 10px;
        background-color: transparent;
        color: #CBD5E1 !important;
        text-align: left;
        padding: 10px 15px;
        margin: 4px 0;
        font-size: 15px;
        font-weight: 500;
        transition: 0.2s;
    }

    [data-testid="stSidebar"] .stButton > button:hover {
        background-color: #334155;
        color: #FFFFFF !important;
        border: 1px solid #475569;
    }

    /* Sidebar footer */
    .sidebar-footer {
        margin-top: 35px;
        padding: 15px;
        border-radius: 12px;
        background-color: #334155;
        color: #CBD5E1 !important;
        font-size: 12px;
        text-align: center;
        line-height: 1.7;
    }

    /* KPI cards */
    [data-testid="stMetric"] {
        background-color: #1E293B !important;
        border: 1px solid #334155 !important;
        padding: 18px !important;
        border-radius: 12px !important;
        box-shadow: 0 4px 10px rgba(0, 0, 0, 0.15);
        overflow: hidden !important;
    }

    /* KPI labels */
    [data-testid="stMetricLabel"] {
        color: #CBD5E1 !important;
        font-size: 14px !important;
    }

    /* KPI values */
    [data-testid="stMetricValue"] {
        color: #FFFFFF !important;
        font-size: 25px !important;
        font-weight: 700 !important;
        white-space: nowrap !important;
        overflow: hidden !important;
        text-overflow: ellipsis !important;
    }

    /* KPI delta */
    [data-testid="stMetricDelta"] {
        color: #38BDF8 !important;
    }

    /* General headings */
    h1, h2, h3, h4, h5, h6 {
        color: #FFFFFF !important;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# =========================================================
# SIDEBAR NAVIGATION
# =========================================================

with st.sidebar:

    st.markdown(
        '<div class="sidebar-title">🏦 Banking Analytics</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="sidebar-subtitle">Financial Intelligence Dashboard</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="sidebar-section">Main Menu</div>',
        unsafe_allow_html=True
    )

    if st.button("📊  Overview", use_container_width=True):
        change_page("Overview")

    if st.button("💳  Transactions", use_container_width=True):
        change_page("Transactions")

    if st.button("👥  Customers", use_container_width=True):
        change_page("Customers")

    if st.button("💰  Loans", use_container_width=True):
        change_page("Loans")

    st.markdown("---")

    st.markdown(
        """
        <div class="sidebar-footer">
            <b>Banking Analytics Project</b><br>
            Powered by Streamlit, Plotly and Gemini AI
        </div>
        """,
        unsafe_allow_html=True
    )


page = st.session_state.page


# =========================================================
# COMMON DATA
# =========================================================

transactions = analysis.transactions.copy()
loan = analysis.loan.copy()
rfm = analysis.rfm.copy()


# =========================================================
# OVERVIEW PAGE
# =========================================================

if page == "Overview":

    st.markdown(
        '<div class="main-title">Banking Analytics Dashboard</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="sub-title">Overview of transactions, customers and loans</div>',
        unsafe_allow_html=True
    )

    st.divider()

    # =====================================================
    # KPI CARDS
    # =====================================================

    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.metric(
            "Successful Amount",
            format_amount(
                analysis.total_successful_transactions_amount
            )
        )

    with col2:
        st.metric(
            "Successful Transactions",
            f"{analysis.total_successful_transactions_count:,}"
        )

    with col3:
        st.metric(
            "Success Rate",
            f"{analysis.percentage_success:.2f}%"
        )

    with col4:
        st.metric(
            "Active Customers",
            f"{analysis.no_of_active_customer:,}"
        )

    with col5:
        st.metric(
            "Loan Applications",
            f"{analysis.total_loan_applications:,}"
        )

    st.write("")

    # =====================================================
    # GEMINI AI BUSINESS INSIGHTS
    # =====================================================

    st.subheader("🤖 AI-Powered Business Insights")

    st.write(
        "Generate a business analysis using the banking metrics "
        "available in this dashboard."
    )

    if st.button(
        "✨ Generate AI Business Insights",
        type="primary",
        use_container_width=False
    ):
        generate_ai_insights()

    if st.session_state.ai_insights is not None:

        st.markdown(
            "### Gemini Analysis"
        )

        st.markdown(
            st.session_state.ai_insights
        )

    st.divider()

    # =====================================================
    # MONTHLY TREND AND TRANSACTION STATUS
    # =====================================================

    left_col, right_col = st.columns([2, 1])

    with left_col:

        st.subheader("Monthly Transaction Trend")

        monthly_data = (
            analysis.year_month_wise_analysis
            .reset_index()
        )

        monthly_data["month_year"] = (
            monthly_data["month"]
            + " "
            + monthly_data["year"].astype(str)
        )

        fig_monthly = px.line(
            monthly_data,
            x="month_year",
            y="total_amount",
            markers=True,
            title="Successful Transaction Amount by Month"
        )

        fig_monthly.update_layout(
            height=380,
            xaxis_title="Month",
            yaxis_title="Amount",
            showlegend=False
        )

        st.plotly_chart(
            fig_monthly,
            use_container_width=True
        )

    with right_col:

        st.subheader("Transaction Status")

        status_data = (
            transactions["transaction_status"]
            .value_counts()
            .reset_index()
        )

        status_data.columns = [
            "status",
            "count"
        ]

        fig_status = px.pie(
            status_data,
            names="status",
            values="count",
            hole=0.55,
            title="Transaction Status Distribution"
        )

        fig_status.update_layout(
            height=380
        )

        st.plotly_chart(
            fig_status,
            use_container_width=True
        )

    # =====================================================
    # MERCHANT AND LOAN STATUS
    # =====================================================

    left_col, right_col = st.columns(2)

    with left_col:

        st.subheader("Top Merchant Categories")

        merchant_data = (
            analysis.merchant_category_analysis
            .reset_index()
            .head(10)
        )

        fig_merchant = px.bar(
            merchant_data,
            x="total_amount",
            y="merchant_category",
            orientation="h",
            title="Top Merchant Categories by Amount"
        )

        fig_merchant.update_layout(
            height=400,
            yaxis_title="Merchant Category",
            xaxis_title="Total Amount"
        )

        st.plotly_chart(
            fig_merchant,
            use_container_width=True
        )

    with right_col:

        st.subheader("Loan Status")

        loan_status_data = (
            loan["loan_status"]
            .value_counts()
            .reset_index()
        )

        loan_status_data.columns = [
            "loan_status",
            "count"
        ]

        fig_loan_status = px.bar(
            loan_status_data,
            x="loan_status",
            y="count",
            title="Loan Applications by Status"
        )

        fig_loan_status.update_layout(
            height=400,
            xaxis_title="Loan Status",
            yaxis_title="Number of Applications"
        )

        st.plotly_chart(
            fig_loan_status,
            use_container_width=True
        )


# =========================================================
# TRANSACTIONS PAGE
# =========================================================

elif page == "Transactions":

    st.title("💳 Transaction Analysis")

    st.write(
        "Detailed analysis of successful transactions, payment modes "
        "and merchant categories."
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Average Successful Transaction",
            format_amount(
                analysis.avg_successful_transactions_amount
            )
        )

    with col2:
        st.metric(
            "Total Transactions",
            f"{transactions['transaction_id'].nunique():,}"
        )

    with col3:
        st.metric(
            "Failed Transactions",
            f"{(transactions['transaction_status'] == 'Failed').sum():,}"
        )

    st.divider()

    left_col, right_col = st.columns(2)

    with left_col:

        st.subheader("Payment Mode Analysis")

        payment_data = (
            analysis.payment_analysis
            .reset_index()
        )

        fig_payment = px.bar(
            payment_data,
            x="payment_mode",
            y="total_amount",
            title="Amount by Payment Mode"
        )

        st.plotly_chart(
            fig_payment,
            use_container_width=True
        )

    with right_col:

        st.subheader("City-wise Transaction Amount")

        city_data = (
            analysis.city_analysis
            .reset_index()
        )

        fig_city = px.bar(
            city_data,
            x="city",
            y="total_amount",
            title="Top Cities by Transaction Amount"
        )

        st.plotly_chart(
            fig_city,
            use_container_width=True
        )

    st.subheader("Payment Mode Failure Rate")

    failure_data = (
        analysis.payment_vs_transaction_status_analysis
        .reset_index()
    )

    fig_failure = px.bar(
        failure_data,
        x="payment_mode",
        y="failure_rate",
        title="Failure Rate by Payment Mode"
    )

    fig_failure.update_layout(
        yaxis_title="Failure Rate (%)"
    )

    st.plotly_chart(
        fig_failure,
        use_container_width=True
    )

    st.subheader("Transaction Data")

    st.dataframe(
        transactions,
        use_container_width=True
    )


# =========================================================
# CUSTOMERS PAGE
# =========================================================

elif page == "Customers":

    st.title("👥 Customer and RFM Analysis")

    st.write(
        "Customer segmentation based on Recency, Frequency and Monetary value."
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Total Customers",
            f"{rfm['customer_id'].nunique():,}"
        )

    with col2:
        st.metric(
            "Customer Segments",
            f"{rfm['segment'].nunique():,}"
        )

    with col3:
        st.metric(
            "Highest Customer Value",
            format_amount(
                rfm["monetary"].max()
            )
        )

    st.divider()

    left_col, right_col = st.columns(2)

    with left_col:

        st.subheader("Customer Segment Distribution")

        segment_data = (
            rfm["segment"]
            .value_counts()
            .reset_index()
        )

        segment_data.columns = [
            "segment",
            "customer_count"
        ]

        fig_segment = px.pie(
            segment_data,
            names="segment",
            values="customer_count",
            hole=0.5,
            title="Customers by Segment"
        )

        st.plotly_chart(
            fig_segment,
            use_container_width=True
        )

    with right_col:

        st.subheader("Segment-wise Monetary Value")

        segment_amount_data = (
            analysis.segment_analysis
            .reset_index()
        )

        fig_segment_amount = px.bar(
            segment_amount_data,
            x="segment",
            y="total_amount_per_segment",
            title="Total Amount by Customer Segment"
        )

        st.plotly_chart(
            fig_segment_amount,
            use_container_width=True
        )

    st.subheader("Highest Value Customers")

    st.dataframe(
        analysis.highest_value_customer,
        use_container_width=True
    )

    st.subheader("Complete RFM Data")

    st.dataframe(
        rfm,
        use_container_width=True
    )


# =========================================================
# LOANS PAGE
# =========================================================

elif page == "Loans":

    st.title("💰 Loan Analysis")

    st.write(
        "Analysis of loan applications, approval amounts, credit scores "
        "and repayment burden."
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Loan Applications",
            f"{analysis.total_loan_applications:,}"
        )

    with col2:
        st.metric(
            "Requested Amount",
            format_amount(
                analysis.total_requested_loan_amount
            )
        )

    with col3:
        st.metric(
            "Approved Amount",
            format_amount(
                analysis.total_approved_loan_amount
            )
        )

    st.divider()

    left_col, right_col = st.columns(2)

    with left_col:

        st.subheader("Loan Type Analysis")

        loan_type_data = (
            analysis.loan_category_analysis
            .reset_index()
        )

        fig_loan_type = px.bar(
            loan_type_data,
            x="loan_type",
            y="no_of_applications",
            title="Applications by Loan Type"
        )

        st.plotly_chart(
            fig_loan_type,
            use_container_width=True
        )

    with right_col:

        st.subheader("Credit Score Category")

        credit_data = (
            analysis.credit_score_category_analysis
            .reset_index()
        )

        credit_columns = [
            column
            for column in credit_data.columns
            if column != "credit_score_category"
        ]

        fig_credit = px.bar(
            credit_data,
            x="credit_score_category",
            y=credit_columns,
            title="Loan Status by Credit Score Category",
            barmode="group"
        )

        st.plotly_chart(
            fig_credit,
            use_container_width=True
        )

    left_col, right_col = st.columns(2)

    with left_col:

        st.subheader("EMI Burden Distribution")

        burden_data = (
            loan["burden_type"]
            .value_counts()
            .reset_index()
        )

        burden_data.columns = [
            "burden_type",
            "count"
        ]

        fig_burden = px.pie(
            burden_data,
            names="burden_type",
            values="count",
            hole=0.5,
            title="Loans by EMI Burden"
        )

        st.plotly_chart(
            fig_burden,
            use_container_width=True
        )

    with right_col:

        st.subheader("Repayment Status")

        repayment_data = (
            loan["repayment_status"]
            .value_counts()
            .reset_index()
        )

        repayment_data.columns = [
            "repayment_status",
            "count"
        ]

        fig_repayment = px.bar(
            repayment_data,
            x="repayment_status",
            y="count",
            title="Loan Repayment Status"
        )

        st.plotly_chart(
            fig_repayment,
            use_container_width=True
        )

    st.subheader("Loan Data")

    st.dataframe(
        loan,
        use_container_width=True
    )