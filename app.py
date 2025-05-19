import streamlit as st
from datetime import datetime
from utils.background import set_background
from utils.helper import get_location, get_weather, get_news, format_news_report
from utils.constans import CATEGORIES
from agents.ai_agent import run_ai_crew
from agents.financial_agent import fetch_ai_news

# Set layout and background
st.set_page_config(layout="wide", page_title="PulseWire", page_icon="📰")
set_background("news1.jpg")

# Navigation setup
query_params = st.query_params
page_param = query_params.get("page", ["home"])
page = page_param[0] if isinstance(page_param, list) else page_param
page = page if page in ["home", "agent", "fins"] else "home"
st.session_state.page = page

# Init session
if "selected_cat" not in st.session_state:
    st.session_state.selected_cat = "general"

# Navbar
st.markdown("""
<div class="nav-container">
    <form method="get"><input type="hidden" name="page" value="home"/>
    <button type="submit">🏠 Home</button></form>
    <form method="get"><input type="hidden" name="page" value="agent"/>
    <button type="submit">🧠 Agent</button></form>
    <form method="get"><input type="hidden" name="page" value="fins"/>
    <button type="submit">📈 Financial News Agent</button></form>
</div>
<style>
.nav-container {display: flex; gap: 0.75rem; margin-bottom: 1.5rem;}
.nav-container button {
    background-color: #000; color: white;
    padding: 0.5rem 1.2rem; border: none;
    border-radius: 8px; font-size: 1rem; cursor: pointer;
}
.nav-container button:hover {background-color: #222;}
</style>
""", unsafe_allow_html=True)

# ========== HOME PAGE ==========
if page == "home":
    location = get_location()
    weather = get_weather(location)
    today = datetime.now().strftime("%A, %d %B %Y")

    st.markdown(f"""
    <div style='background-color:#1f1f1f;padding:1rem 2rem;border-radius:10px;margin-bottom:1.5rem;display:flex;justify-content:space-between;flex-wrap:wrap;'>
        <div style='font-size:2.5rem;font-weight:700;color:white;'>📰 PulseWire</div>
        <div style='text-align:right;color:#ddd;font-size:1.1rem;'>
            📍 <strong>{location}</strong> &nbsp;|&nbsp;
            🌤️ {weather} &nbsp;|&nbsp;
            📅 {today}
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.write("### Select News Category")
    st.markdown("""
<style>
div.stButton > button {
    background-color: black; color: white;
    border-radius: 6px; padding: 0.5rem 1rem;
    font-weight: bold; border: 1px solid #444;
    width: 100%;
}
div.stButton > button:hover {background-color: #222;}
.selected-button {
    background-color: yellow !important;
    color: black !important;
}
</style>
""", unsafe_allow_html=True)

    # Buttons
    cols = st.columns(len(CATEGORIES))
    for idx, cat in enumerate(CATEGORIES):
        label = cat.capitalize()
        if cols[idx].button(label, key=f"cat_{cat}"):
            st.session_state.selected_cat = cat

    # Top story and more
    articles = get_news(st.session_state.selected_cat)
    if articles:
        st.subheader("🏆 Top Story")
        top = articles[0]
        cols = st.columns([2, 1])
        with cols[0]:
            st.markdown(f"### {top['title']}")
            st.caption(f"{top.get('source', {}).get('name', '')} | {top.get('author', 'Unknown')} | {top.get('publishedAt', '')[:10]}")
            st.write(top.get("description", "No description."))
        with cols[1]:
            if top.get("urlToImage"):
                st.image(top["urlToImage"], use_container_width=True)

        st.markdown("---")
        st.subheader("📰 More Stories")
        for i in range(1, len(articles), 3):
            row = st.columns(3)
            for j in range(3):
                if i + j < len(articles):
                    a = articles[i + j]
                    with row[j]:
                        if a.get("urlToImage"):
                            st.image(a["urlToImage"], use_container_width=True)
                        st.markdown(f"**{a['title']}**")
                        st.caption(f"{a.get('source', {}).get('name')} | {a.get('publishedAt', '')[:10]}")
                        st.markdown(f"[Read more]({a['url']})", unsafe_allow_html=True)
    else:
        st.warning("No articles found.")

# ========== AGENT PAGE ==========
elif page == "agent":
    st.markdown("### 🔍 Ask Our AI Journalist")
    query = st.text_input("Enter a topic like 'AI and healthcare'", key="ai_journalist_query")
    if st.button("🚀 Generate AI-Powered Summary"):
        if not query.strip():
            st.warning("⚠️ Please enter a valid topic.")
        else:
            location = get_location()
            weather = get_weather(location)
            with st.spinner("🧠 Running the AI crew..."):
                report = run_ai_crew(query, location, weather)
                if report:
                    st.success("✅ Crew finished executing.")
                    st.markdown("### 📝 Final Report")
                    st.markdown(report, unsafe_allow_html=True)
                    st.download_button("📥 Download Report", data=report, file_name="report.md", mime="text/markdown")
                else:
                    st.warning("⚠️ No markdown output found.")

# ========== FINS PAGE ==========
elif page == "fins":
    st.title("📈 Financial News Agent")
    query = st.text_input("Query:", value="Tesla earnings news")
    if st.button("🔍 Get Financial News"):
        with st.spinner("Gathering news..."):
            try:
                result = fetch_ai_news(query)
                st.markdown(result, unsafe_allow_html=True)
            except Exception as e:
                st.error(f"Error: {e}")
