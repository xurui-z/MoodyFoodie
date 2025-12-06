import streamlit as st
import time

# Import our core logic
# Note: On the first run, this will take a few seconds to load data (Loading data...)
import agent_logic_google as agent_logic

# === Page Configuration ===
st.set_page_config(
    page_title="MoodBites Chef",
    page_icon="🍲",
    layout="centered"
)

# === Sidebar Design ===
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/1830/1830839.png", width=100)
    st.title("MoodBites 🌿")
    st.markdown("---")
    st.write("**How it works:**")
    st.write("1. Tell us how you feel.")
    st.write("2. AI searches 5,000+ recipes.")
    st.write("3. Get a meal plan matching your vibe.")
    st.markdown("---")
    st.caption("Powered by Gemini & RAG Technology")

# === Main Page Design ===
st.title("🍳 Mood-Based Meal Planner")
st.markdown("Don't know what to eat? Let your **mood** decide.")

# User Input Area
user_mood = st.text_area(
    "How are you feeling right now?",
    placeholder="e.g., I had a stressful week and I want something warm and cozy...",
    height=100
)

# Button Logic
if st.button("Generate My Meal Plan ✨", type="primary"):
    if not user_mood:
        st.warning("Please tell me your mood first!")
    else:
        # Show loading animation
        with st.spinner("👩‍🍳 Chef AI is reading your mood and searching recipes..."):
            try:
                # 1. Call the function we wrote in agent_logic
                # start_time = time.time()
                response = agent_logic.generate_mood_plan(user_mood)
                
                # 2. Simulate typewriter effect (Optional, for fun)
                # time.sleep(1) 
                
                # 3. Display results
                st.success("Meal Plan Ready!")
                st.markdown("---")
                
                # Render the beautiful text returned by AI using Markdown
                st.markdown(response)
                
            except Exception as e:
                st.error(f"An error occurred: {e}")

# === Footer ===
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: grey;'>NLP Course Project | Context-Aware Food Recommendation</div>", 
    unsafe_allow_html=True
)