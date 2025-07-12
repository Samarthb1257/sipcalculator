import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from io import BytesIO

st.set_page_config(page_title="Become A Crorepati Calculator", layout="centered")

st.title("💰 Become A Crorepati Calculator")

st.markdown("""
This calculator helps you calculate how much money you need to save monthly to become a Crorepati 💸  
Check out the Top SIP (Systematic Investment Plan) mutual fund schemes to invest.
""")

# --- Inputs ---
target_amount = st.number_input("🏁 Target Amount to Become Crorepati (₹)", value=50000000, step=1000000, format="%d")
current_age = st.slider("🎂 Your Current Age", 10, 100, 25)
target_age = st.slider("🎯 Age When You Want to Become Crorepati", current_age + 1, 100, 60)
inflation_rate = st.slider("📈 Expected Inflation Rate (% per annum)", 0.0, 10.0, 0.0, 0.1)
return_rate = st.slider("📊 Expected SIP Return Rate (% per annum)", 5.0, 20.0, 13.0, 0.1)
current_savings = st.number_input("💼 Current Savings (₹)", value=0, step=100000, format="%d")

# --- Calculations ---
years_to_invest = target_age - current_age
inflation_adjusted_target = target_amount * ((1 + inflation_rate / 100) ** years_to_invest)
future_value_savings = current_savings * ((1 + return_rate / 100) ** years_to_invest)
sip_target = inflation_adjusted_target - future_value_savings

monthly_rate = return_rate / (12 * 100)
n_months = years_to_invest * 12

# SIP Calculation Formula
if monthly_rate == 0:
    monthly_sip = sip_target / n_months
else:
    monthly_sip = sip_target * monthly_rate / ((1 + monthly_rate) ** n_months - 1)

total_invested = monthly_sip * n_months
total_growth = sip_target - total_invested

# --- Display Summary ---
st.subheader("📋 Summary of Your SIP Journey")

col1, col2 = st.columns(2)
col1.metric("🎯 Inflation Adjusted Target", f"₹ {inflation_adjusted_target:,.0f}")
col2.metric("💹 Growth from Current Savings", f"₹ {future_value_savings:,.0f}")
col1.metric("⏳ Years to Invest", f"{years_to_invest} Years")
col2.metric("💸 Monthly SIP Required", f"₹ {monthly_sip:,.0f}")
col1.metric("📥 Total SIP Investment", f"₹ {total_invested:,.0f}")
col2.metric("📈 Total Growth", f"₹ {total_growth:,.0f}")

# --- Choose Action ---
option = st.radio("Choose Action", ["📄 Download Excel", "📊 Show Chart"])

# --- Excel Download ---
if option == "📄 Download Excel":
    df = pd.DataFrame({
        "Description": [
            "Target Amount",
            "Inflation Adjusted Target",
            "Current Age",
            "Target Age",
            "Years to Save",
            "Inflation Rate (%)",
            "Return Rate (%)",
            "Current Savings",
            "Growth from Savings",
            "Monthly SIP Required",
            "Total SIP Invested",
            "Total Growth"
        ],
        "Value": [
            f"₹ {target_amount:,.0f}",
            f"₹ {inflation_adjusted_target:,.0f}",
            f"{current_age}",
            f"{target_age}",
            f"{years_to_invest}",
            f"{inflation_rate:.2f}%",
            f"{return_rate:.2f}%",
            f"₹ {current_savings:,.0f}",
            f"₹ {future_value_savings:,.0f}",
            f"₹ {monthly_sip:,.0f}",
            f"₹ {total_invested:,.0f}",
            f"₹ {total_growth:,.0f}"
        ]
    })

    output = BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name="Crorepati SIP")
        writer.close()

    st.download_button(
        label="📥 Download SIP Summary as Excel",
        data=output.getvalue(),
        file_name="crorepati_sip_summary.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

# --- Visualization ---
elif option == "📊 Show Chart":
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.bar(["Total Invested", "Total Growth"], [total_invested, total_growth], color=["skyblue", "lightgreen"])
    ax.set_ylabel("Amount (₹)")
    ax.set_title("SIP Investment vs Growth")
    for i, v in enumerate([total_invested, total_growth]):
        ax.text(i, v + 100000, f"₹{v:,.0f}", ha='center')
    st.pyplot(fig)
