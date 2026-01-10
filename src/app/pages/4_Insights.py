import streamlit as st

def insights_page():
    st.title("🧠 Insights & Policy Implications")

    st.markdown("""
### 📌 Aadhaar Updates as a Proxy for Internal Mobility  

Aadhaar demographic & biometric updates capture **frequent changes in address, school, employment, and contact information**, making them a high-resolution proxy for:  

- **Education-driven mobility**  
- **Early career migration**
- **Urban absorption**
- **District-level transition patterns**

Compared to traditional migration statistics (Census, NSSO), Aadhaar updates offer:  

✔ Higher temporal resolution (monthly)  
✔ District granularity (1046 districts)  
✔ Age-structured signals  
✔ Leading indicators for planning  
""")

    st.markdown("""
### 🎓 Education as the Largest Driver of Mobility  

Our forecasting results show that **student mobility is highly predictable** (low RMSE), indicating that education transitions such as:

- Enrollment in higher secondary
- Coaching & test preparation
- College & technical education
- Skill training & certification

generate persistent and structured Aadhaar demographic activity.

This highlights the emergence of **education hubs** in Tier-2/Tier-3 districts.
""")

    st.markdown("""
### 🏙️ Migration, Workforce & Urban Absorption

Movement forecasting reveals high concentration of mobility in established metros, but **per-capita analysis identifies emerging urban nodes** absorbing student and early workforce flows.

These districts contribute to:

✔ Skill pipeline formation  
✔ Housing & transit demand  
✔ Digital identity usage  
✔ Local employment transitions  
""")

    st.markdown("""
### 🔮 Why Forecasting Mobility Matters for Planning

A 3-month forecast horizon supports **anticipatory planning** in:

- **Education capacity**
- **Urban transport**
- **Housing markets**
- **Digital service delivery**
- **Identity infrastructure**
- **Skill training allocation**
- **State-level budgeting**

Rather than reacting to migration patterns, planners can **anticipate shifts**.
""")

    st.markdown("""
### 🗺️ District-Level Granularity Enables Targeted Interventions

District forecasts highlight:

✔ Rising student hubs  
✔ Emerging urban nodes  
✔ Stable districts  
✔ Out-migration belts  

Such patterns support **differentiated policy**, recognizing that:

> India’s internal migration is not uniform; it is **age-structured**, **education-led**, and **district-specific**.
""")

    st.markdown("""
### 📍 Proposed Use Cases for System Improvement

This dashboard can support:

1. **Education Planning**
   - forecasting school/college demand

2. **Skill Ecosystem Planning**
   - anticipating training & coaching migration

3. **Urban Capacity Planning**
   - transport, housing, digital services

4. **State Coordination**
   - migration corridors between states

5. **Aadhaar System Optimization**
   - load forecasting for demographic/biometric updates

""")

    st.markdown("""
### 🧩 Method Summary (Short)

- **Phase-1:** Data ingestion + cleaning  
- **Phase-2:** Monthly mobility signal extraction  
- **Phase-3:** Clustering (Mobility Archetypes) *(optional for demo)*  
- **Phase-4:** 3-month forecasting (Random Forest)  
- **Phase-5:** Decision Dashboard (Streamlit + Plotly)  
""")

    st.markdown("""
---
### 🇮🇳 Broader Implication

Aadhaar updates represent one of India’s **richest real-time signals** for internal movement dynamics.  

Understanding these patterns can support:

- social development,
- economic planning,
- infrastructure deployment,
- and identity system improvement.

This aligns directly with the hackathon’s goal:
> “Unlock societal trends to support informed decision-making & system improvements.”
""")

if __name__ == "__main__":
    insights_page()
