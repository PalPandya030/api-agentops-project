import streamlit as st
import requests
import pandas as pd

# ------------------- PAGE CONFIG -------------------
st.set_page_config(page_title="AI Marketplace", layout="wide")

# ------------------- CUSTOM CSS -------------------
st.markdown("""
<style>
body {
    background-color: #0E1117;
    color: white;
}

.card {
    background: #1c1f26;
    padding: 15px;
    border-radius: 12px;
    margin-bottom: 10px;
    box-shadow: 0px 4px 15px rgba(0,0,0,0.4);
}

.title {
    font-size: 32px;
    font-weight: bold;
    color: #4CAF50;
}

.subtitle {
    color: #9ca3af;
}
</style>
""", unsafe_allow_html=True)

# ------------------- HEADER -------------------
st.markdown('<div class="title">🤖 AI Service Marketplace</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Smart API Negotiation System</div>', unsafe_allow_html=True)

# ------------------- SIDEBAR -------------------
menu = st.sidebar.radio("Navigation", ["Dashboard", "Negotiation", "History"])

# ------------------- DASHBOARD -------------------
if menu == "Dashboard":
    st.markdown("## 📊 Dashboard")

    col1, col2, col3 = st.columns(3)

    col1.markdown('<div class="card">💼 Active Deals<br><h2>12</h2></div>', unsafe_allow_html=True)
    col2.markdown('<div class="card">💰 Savings<br><h2>$230</h2></div>', unsafe_allow_html=True)
    col3.markdown('<div class="card">✅ Success Rate<br><h2>92%</h2></div>', unsafe_allow_html=True)

    st.markdown("### 📈 Trends")
    st.line_chart([10, 20, 15, 30, 25, 40])

# ------------------- NEGOTIATION -------------------
elif menu == "Negotiation":
    st.markdown("## 🤝 AI Negotiation Chat")

    # Chat memory
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Show previous messages
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # Suggestions
    st.markdown("### 💡 Suggestions")
    col1, col2, col3 = st.columns(3)

    if col1.button("⚡ cheap fast api in india"):
        user_input = "cheap fast api in india"
    elif col2.button("🎯 high accuracy global api"):
        user_input = "high accuracy global api"
    elif col3.button("💰 low cost high throughput api"):
        user_input = "low cost high throughput api"
    else:
        user_input = st.chat_input("Type your requirement...")

    if user_input:
        # Add user message
        st.session_state.messages.append({"role": "user", "content": user_input})

        with st.chat_message("user"):
            st.markdown(user_input)

        try:
            response = requests.post(
                "http://localhost:8000/negotiate",
                params={"user_input": user_input}
            )

            data = response.json()

            # ------------------- AI RESPONSE -------------------
            with st.chat_message("assistant"):

                st.markdown("## 🏆 Top API Matches")

                for i, api in enumerate(data["top_apis"], 1):
                    st.markdown(f"""
                    <div class="card">
                    <b>#{i} {api['name']}</b><br>
                    💰 Price: ${api['price']} <br>
                    ⚡ Latency: {api['latency']} ms <br>
                    🎯 Accuracy: {api['accuracy']}% <br>
                    🚀 Throughput: {api['throughput']}
                    </div>
                    """, unsafe_allow_html=True)

                # ------------------- TABLE -------------------
                df = pd.DataFrame(data["top_apis"])

                st.markdown("### 📊 Comparison Table")
                st.dataframe(df)

                # ------------------- CHART -------------------
                st.markdown("### 📈 Price vs Latency")
                st.line_chart(df[["price", "latency"]])

                # ------------------- FINAL RESULT -------------------
                st.markdown("## 🎯 Final Deal")

                col1, col2, col3 = st.columns(3)

                col1.metric("API", data["selected_api"])
                col2.metric("Original Price", f"${data['original_price']}")
                col3.metric("Final Price", f"${data['final_price']}")

                st.markdown("### 📊 Monitoring")
                st.json(data["monitoring"])

        except:
            st.error("❌ Backend not running!")

# ------------------- HISTORY -------------------
elif menu == "History":
    st.markdown("## 📜 History")

    if st.button("🔄 Load History"):
        try:
            res = requests.get("http://localhost:8000/history")
            history = res.json()

            if not history:
                st.info("No deals yet.")
            else:
                for deal in history[::-1]:
                    st.markdown(f"""
                    <div class="card">
                    <b>{deal['selected_api']}</b><br>
                    Final Price: ${deal['final_price']}
                    </div>
                    """, unsafe_allow_html=True)

        except:
            st.error("❌ Backend not running!")