
import streamlit as st
import requests
import json
from dotenv import load_dotenv
import os
import time
import pandas as pd

load_dotenv()
GEMINI_API_KEY = "AIzaSyBn3LmJbLYp_BypnA2eSd5YC2kim3wlUWo"

SYSTEM_PROMPT = """
You are Sparkle, an AI health coach. Your role is to assist users with health-related queries in a friendly, supportive, and intelligent way.

You are capable of providing personalized guidance and educational support on:

🛌 Sleep & Rest:
- Sleep habits and how to improve sleep quality
- Sleep hygiene and routines

💧 Hydration & Nutrition:
- Water intake goals and hydration habits
- Macronutrients (carbs, protein, fats) explained in simple terms
- Meal planning tips (e.g., diabetic-friendly, low-carb, heart-healthy)
- Sample healthy food or snack ideas

🏃 Physical Activity & Health Goals:
- Daily step count tracking
- Personalized fitness suggestions
- Health goal tracking (e.g., “I want to walk 10,000 steps a day”)
- Safe exercise and injury prevention

🙂 Mood & Mental Well-being:
- Mood tracking and emotional patterns
- Stress management tips
- Breathing exercises and mindfulness practices
- Recognizing signs of burnout and self-care suggestions

🧪 Medical Literacy (non-diagnostic):
- Common medications (tablets, syrups, powders, injections, insulins, etc.)
- Medical devices and their usage (e.g., glucometers, BP monitors)
- Founders or inventors of medical breakthroughs or pharma companies
- Differences between generic and branded medicines
- Basics of lab tests and their interpretations (e.g., HbA1c, BMI)
- Awareness of chronic conditions like diabetes or hypertension
- Public health topics like vaccines, disease prevention, first aid

📱 Health-Tech & Modern Care:
- Digital health innovations (e.g., wearables, smart health apps)
- AI in healthcare and robotic diagnostics
- Benefits of telemedicine

🌿 Environmental & Holistic Wellness:
- Benefits of sunlight, walking, and green spaces
- Effects of pollution on respiratory health
- Digital detox and reducing screen time

💡 If the user asks about **personal health insights** (e.g., “How am I doing?”, “Show my weekly summary”), and no health data has been provided yet, kindly inform them to upload or generate their insights first.

❌ If the user's query is **not related to health, wellness, medicine, or the medical industry**, politely let them know that you are only trained to handle health-related topics and suggest they ask something in that area.

Always personalize your responses based on the user’s intent and the available insights. Be empathetic, motivational, and avoid generic replies. Your tone should be encouraging and human-like, just like a friendly wellness coach.
"""

def ask_gemini(user_message, chat_history, user_insights):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={GEMINI_API_KEY}"

    conversation = ""
    for sender, msg in chat_history:
        role = "User" if sender == "You" else "Sparkle"
        conversation += f"{role}: {msg}\n"

    if user_insights is not None:
        if isinstance(user_insights, pd.DataFrame):  # If it's a DataFrame
            if not user_insights.empty:  # Check if the DataFrame is not empty
                conversation += f"User Insights (Hydration Log): {user_insights.to_string()}\n"
        elif isinstance(user_insights, dict):  # If it's a JSON object
            conversation += f"User Insights: {json.dumps(user_insights)}\n"
        elif isinstance(user_insights, str):  # If it's plain text
            conversation += f"User Insights: {user_insights}\n"
        
    conversation += f"User: {user_message}\nSparkle:"

    prompt = f"{SYSTEM_PROMPT}\n\n{conversation}"

    headers = {"Content-Type": "application/json"}
    data = {
        "contents": [
            {
                "parts": [{"text": prompt}]
            }
        ]
    }

    try:
        response = requests.post(url, headers=headers, data=json.dumps(data))
        response.raise_for_status()
        gemini_reply = response.json()["candidates"][0]["content"]["parts"][0]["text"]
        return gemini_reply.strip()
    except Exception as e:
        return f"⚠️ Gemini API error: {e}"

st.set_page_config(page_title="Vita AI Health Chatbot", layout="centered")
st.title("🤖 Vita : AI Health Chatbot")
st.caption("Chat with Vita about health, wellness, healthcare, health products, and more.")

with st.container():
    uploaded_file = st.file_uploader("Upload Health Insights File (TXT, CSV, JSON)", type=["txt", "csv", "json"])

user_insights = None

if uploaded_file:
    if uploaded_file.type == "text/plain":
        user_insights = uploaded_file.getvalue().decode("utf-8") 
    elif uploaded_file.type == "application/json":
        user_insights = json.loads(uploaded_file.getvalue().decode("utf-8")) 
    elif uploaded_file.type == "text/csv":
        user_insights = pd.read_csv(uploaded_file) 

    st.write("Uploaded Insights:")
    st.write(user_insights)


if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "pending_message" not in st.session_state:
    st.session_state.pending_message = None

with st.container():
    # st.markdown("### 🗨️ Health Chat")
    chat_area = st.container()
    with chat_area:
        for sender, msg in st.session_state.chat_history:
            emoji = "❓" if sender == "You" else "🔍"
            with st.chat_message(emoji):
                st.markdown(msg)

        if st.session_state.pending_message:
            with st.chat_message("🔍"):
                with st.spinner("Vita is thinking..."):
                    time.sleep(1.5)
                    st.markdown(st.session_state.pending_message)
            st.session_state.chat_history.append(("Vita", st.session_state.pending_message))
            st.session_state.pending_message = None
            st.rerun()

with st.container():
    with st.form(key="chat_input_form", clear_on_submit=True):
        user_query = st.text_input("💬 Type your message", key="user_input")
        submitted = st.form_submit_button("Send")

    if submitted and user_query:
        st.session_state.chat_history.append(("You", user_query))
        gemini_reply = ask_gemini(user_query, st.session_state.chat_history, user_insights)
        st.session_state.pending_message = gemini_reply
        st.rerun()

if "chat_history" in st.session_state and st.session_state.chat_history:
    export_text = ""
    for sender, msg in st.session_state.chat_history:
        emoji = "❓" if sender == "You" else "🔍"
        export_text += f"{emoji} {msg}\n\n"

    st.download_button(
        label="📥 Download Chat (.txt)",
        data=export_text,
        file_name="vita_chat.txt",
        mime="text/plain"
    )

# import streamlit as st
# import requests
# import json
# from dotenv import load_dotenv
# import os
# import time

# load_dotenv()
# GEMINI_API_KEY = "AIzaSyBn3LmJbLYp_BypnA2eSd5YC2kim3wlUWo"

# SYSTEM_PROMPT = """
# You are Sparkle, an AI health coach. Your role is to assist users with health-related queries in a friendly, supportive, and intelligent way.

# You are capable of providing personalized guidance and educational support on:

# 🛌 Sleep & Rest:
# - Sleep habits and how to improve sleep quality
# - Sleep hygiene and routines

# 💧 Hydration & Nutrition:
# - Water intake goals and hydration habits
# - Macronutrients (carbs, protein, fats) explained in simple terms
# - Meal planning tips (e.g., diabetic-friendly, low-carb, heart-healthy)
# - Sample healthy food or snack ideas

# 🏃 Physical Activity & Health Goals:
# - Daily step count tracking
# - Personalized fitness suggestions
# - Health goal tracking (e.g., “I want to walk 10,000 steps a day”)
# - Safe exercise and injury prevention

# 🙂 Mood & Mental Well-being:
# - Mood tracking and emotional patterns
# - Stress management tips
# - Breathing exercises and mindfulness practices
# - Recognizing signs of burnout and self-care suggestions

# 🧪 Medical Literacy (non-diagnostic):
# - Common medications (tablets, syrups, powders, injections, insulins, etc.)
# - Medical devices and their usage (e.g., glucometers, BP monitors)
# - Founders or inventors of medical breakthroughs or pharma companies
# - Differences between generic and branded medicines
# - Basics of lab tests and their interpretations (e.g., HbA1c, BMI)
# - Awareness of chronic conditions like diabetes or hypertension
# - Public health topics like vaccines, disease prevention, first aid

# 📱 Health-Tech & Modern Care:
# - Digital health innovations (e.g., wearables, smart health apps)
# - AI in healthcare and robotic diagnostics
# - Benefits of telemedicine

# 🌿 Environmental & Holistic Wellness:
# - Benefits of sunlight, walking, and green spaces
# - Effects of pollution on respiratory health
# - Digital detox and reducing screen time

# 💡 If the user asks about **personal health insights** (e.g., “How am I doing?”, “Show my weekly summary”), and no health data has been provided yet, kindly inform them to upload or generate their insights first.

# ❌ If the user's query is **not related to health, wellness, medicine, or the medical industry**, politely let them know that you are only trained to handle health-related topics and suggest they ask something in that area.

# Always personalize your responses based on the user’s intent and the available insights. Be empathetic, motivational, and avoid generic replies. Your tone should be encouraging and human-like, just like a friendly wellness coach.
# """

# def ask_gemini(user_message, chat_history):
#     url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={GEMINI_API_KEY}"

#     conversation = ""
#     for sender, msg in chat_history:
#         role = "User" if sender == "You" else "Sparkle"
#         conversation += f"{role}: {msg}\n"
#     conversation += f"User: {user_message}\nSparkle:"

#     prompt = f"{SYSTEM_PROMPT}\n\n{conversation}"

#     headers = {"Content-Type": "application/json"}
#     data = {
#         "contents": [
#             {
#                 "parts": [{"text": prompt}]
#             }
#         ]
#     }

#     try:
#         response = requests.post(url, headers=headers, data=json.dumps(data))
#         response.raise_for_status()
#         gemini_reply = response.json()["candidates"][0]["content"]["parts"][0]["text"]
#         return gemini_reply.strip()
#     except Exception as e:
#         return f"⚠️ Gemini API error: {e}"

# st.set_page_config(page_title="Sparkle AI Health Chatbot", layout="centered")
# st.title("🤖 Sparkle: AI Health Chatbot")
# st.caption("Chat with Sparkle about health, wellness, healthcare, health products, and more.")

# with st.container():
#     # st.markdown("### 📝 Please provide your health insights!")
#     st.markdown(
#         "To get more personalized replies, kindly upload insights from the Insight Generator. Once you do, Sparkle can assist you better with your health-related questions!"
#     )


# if "chat_history" not in st.session_state:
#     st.session_state.chat_history = []
# if "pending_message" not in st.session_state:
#     st.session_state.pending_message = None

# with st.container():
#     # st.markdown("### 🗨️ Health Chat")
#     chat_area = st.container()
#     with chat_area:
#         for sender, msg in st.session_state.chat_history:
#             emoji = "❓" if sender == "You" else "🔍"
#             with st.chat_message(emoji):
#                 st.markdown(msg)

#         if st.session_state.pending_message:
#             with st.chat_message("🔍"):
#                 with st.spinner("Sparkle is thinking..."):
#                     time.sleep(1.5)
#                     st.markdown(st.session_state.pending_message)
#             st.session_state.chat_history.append(("Sparkle Bot", st.session_state.pending_message))
#             st.session_state.pending_message = None
#             st.rerun()

# with st.container():
#     with st.form(key="chat_input_form", clear_on_submit=True):
#         user_query = st.text_input("💬 Type your message", key="user_input")
#         submitted = st.form_submit_button("Send")

#     if submitted and user_query:
#         st.session_state.chat_history.append(("You", user_query))
#         gemini_reply = ask_gemini(user_query, st.session_state.chat_history)
#         st.session_state.pending_message = gemini_reply
#         st.rerun()

# if "chat_history" in st.session_state and st.session_state.chat_history:
#     export_text = ""
#     for sender, msg in st.session_state.chat_history:
#         emoji = "❓" if sender == "You" else "🔍"
#         export_text += f"{emoji} {msg}\n\n"

#     st.download_button(
#         label="📥 Download Chat (.txt)",
#         data=export_text,
#         file_name="sparkle_chat.txt",
#         mime="text/plain"
#     )



# # streamlit_chatbot.py placeholder
# # streamlit_chatbot.py

# import streamlit as st
# import pandas as pd
# import matplotlib.pyplot as plt
# from hybrid_insight_engine import generate_combined_insights, load_health_logs
# from trends import plot_health_trends

# st.set_page_config(page_title="Sparkle Health Chatbot", layout="centered")

# st.title("🤖 Sparkle Health Chatbot")
# st.caption("Upload your health logs (CSV) or use demo data and chat with your personal AI wellness assistant.")

# @st.cache_data
# def load_default_data():
#     df = load_health_logs("data/mock_health_logs.csv")
#     insights = generate_combined_insights(df)
#     return df, insights

# def load_uploaded_data(uploaded_file):
#     df = pd.read_csv(uploaded_file, parse_dates=['date'])
#     df.sort_values('date', inplace=True)
#     df['mood'] = df['mood'].str.lower()
#     insights = generate_combined_insights(df)
#     return df, insights

# def get_streamlit_response(user_input, insights, df):
#     user_input = user_input.lower()

#     if "how am i doing" in user_input or "summary" in user_input:
#         return "\n🧠 Summary of Your Health:\n" + "\n".join(f"- {i}" for i in insights)

#     elif "sleep" in user_input:
#         for i in insights:
#             if "sleep" in i.lower():
#                 return f"😴 Sleep Insight:\n- {i}"
#         return "✅ Your sleep looks good!"

#     elif "hydration" in user_input or "water" in user_input:
#         for i in insights:
#             if "hydration" in i.lower() or "water" in i.lower():
#                 return f"🚰 Hydration Insight:\n- {i}"
#         return "✅ Hydration levels are normal."

#     elif "mood" in user_input:
#         for i in insights:
#             if "mood" in i.lower() or "stress" in i.lower():
#                 return f"🧠 Mood Insight:\n- {i}"
#         return "😊 Your mood seems balanced."

#     elif "steps" in user_input or "activity" in user_input:
#         for i in insights:
#             if "step" in i.lower() or "active" in i.lower():
#                 return f"🚶 Activity Insight:\n- {i}"
#         return "✅ Your step count looks healthy."

#     elif "graph" in user_input or "visual" in user_input or "show" in user_input:
#         st.pyplot(plot_health_trends(df))
#         return "📊 Here's your health trend graph!"

#     return "🤖 Sorry, I didn’t get that. Try asking about sleep, mood, hydration, steps, or trends."

# uploaded_file = st.file_uploader("📂 Upload CSV (date, sleep_hours, mood, steps, hydration_ml)", type=["csv"])

# if uploaded_file:
#     df, insights = load_uploaded_data(uploaded_file)
# else:
#     df, insights = load_default_data()

# if "chat_history" not in st.session_state:
#     st.session_state.chat_history = []

# user_query = st.text_input("Ask something like 'How am I doing this week?' or 'Show me my hydration'", key="user_input")

# if user_query:
#     reply = get_streamlit_response(user_query, insights, df)
#     st.session_state.chat_history.append(("You", user_query))
#     st.session_state.chat_history.append(("Sparkle Bot", reply))

# for sender, msg in st.session_state.chat_history:
#     with st.chat_message(sender):
#         st.markdown(msg)
# 👇 Floating chatbot layout with visual styling
# with st.container():
#     st.markdown(
#         """
#         <style>
#         #chatbot-box {
#             position: fixed;
#             bottom: 20px;
#             right: 20px;
#             width: 360px;
#             height: 460px;
#             z-index: 9999;
#             border: 1px solid #ccc;
#             border-radius: 12px;
#             background-color: white;
#             box-shadow: 0 0 20px rgba(0,0,0,0.1);
#             padding: 10px;
#             overflow: auto;
#         }
#         </style>
#         <div id="chatbot-box">
#         <h4>🤖 Sparkle Bot</h4>
#         """,
#         unsafe_allow_html=True
#     )

#     for sender, msg in st.session_state.chat_history[-4:]:  # only show last 4 messages
#         st.chat_message(sender).markdown(msg)

#     user_query = st.text_input("Ask Sparkle Bot...", key="floating_chat_input")
#     if user_query:
#         reply = get_streamlit_response(user_query, insights, df)
#         st.session_state.chat_history.append(("You", user_query))
#         st.session_state.chat_history.append(("Sparkle Bot", reply))




# from fpdf import FPDF
# import io

# def create_chat_pdf(chat_history):
#     pdf = FPDF()
#     pdf.add_page()
#     pdf.set_font("Arial", size=12)

#     for sender, msg in chat_history:
#         emoji = "❓" if sender == "You" else "🔍"
#         text = f"{emoji} {msg}"
#         pdf.multi_cell(0, 10, txt=text)
#         pdf.ln()

#     pdf_buffer = io.BytesIO()
#     pdf.output(pdf_buffer)
#     return pdf_buffer.getvalue()
# if st.button("📄 Download Chat (.pdf)"):
#     pdf_bytes = create_chat_pdf(st.session_state.chat_history)
#     st.download_button(
#         label="📥 Save Chat PDF",
#         data=pdf_bytes,
#         file_name="sparkle_chat.pdf",
#         mime="application/pdf"
#     )

# import streamlit as st
# import pandas as pd
# from hybrid_insight_engine import generate_combined_insights
# from trends import plot_health_trends
# import matplotlib.pyplot as plt
# import requests
# import json
# from dotenv import load_dotenv
# import os

# load_dotenv()
# GEMINI_API_KEY = "AIzaSyBn3LmJbLYp_BypnA2eSd5YC2kim3wlUWo"

# def load_uploaded_data(uploaded_file):
#     df = pd.read_csv(uploaded_file, parse_dates=['date'], dayfirst=True, infer_datetime_format=True)
#     df.sort_values('date', inplace=True)
#     if 'mood' in df.columns:
#         df['mood'] = df['mood'].str.lower()
#     return df

# # used gemini api for chatbot response
# def ask_gemini(user_message, insights):
#     url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={GEMINI_API_KEY}"

#     prompt = f"""
# You are Sparkle, an AI health coach. Here are the user's recent health insights:

# {insights}

# Use these insights to answer the user's health-related questions in a friendly, supportive, and smart way. Be clear and helpful.

# User's question: {user_message}
# """

#     headers = {"Content-Type": "application/json"}
#     data = {
#         "contents": [
#             {
#                 "parts": [{"text": prompt}]
#             }
#         ]
#     }

#     try:
#         response = requests.post(url, headers=headers, data=json.dumps(data))
#         response.raise_for_status()
#         gemini_reply = response.json()["candidates"][0]["content"]["parts"][0]["text"]
#         return gemini_reply
#     except Exception as e:
#         return f"⚠️ Gemini API error: {e}"

# # streamlit website ui
# import streamlit as st
# import time

# st.set_page_config(page_title="Sparkle AI Health Chatbot", layout="centered")
# st.title("🤖 Sparkle: AI Health Chatbot")
# st.caption("Upload your health logs (CSV) and chat with your AI wellness assistant.")

# uploaded_file = st.file_uploader("📂 Upload a CSV (date, sleep_hours, mood, steps, hydration_ml)", type=["csv"])

# if uploaded_file:
#     try:
#         df = load_uploaded_data(uploaded_file)
#         insights = generate_combined_insights(df)

#         if "chat_history" not in st.session_state:
#             st.session_state.chat_history = []
#         if "pending_message" not in st.session_state:
#             st.session_state.pending_message = None

#         with st.container():
#             st.markdown("### 🗨️ ")
#             chat_area = st.container()
#             with chat_area:
#                 for sender, msg in st.session_state.chat_history:
#                     emoji = "❓" if sender == "You" else "🔍"
#                     with st.chat_message(emoji):
#                         st.markdown(msg)

#                 if st.session_state.pending_message:
#                     with st.chat_message("🔍"):
#                         with st.spinner("Sparkle is thinking..."):
#                             time.sleep(1.5)
#                             st.markdown(st.session_state.pending_message)
#                     st.session_state.chat_history.append(("Sparkle Bot", st.session_state.pending_message))
#                     st.session_state.pending_message = None
#                     st.rerun()

#         memory_context = ""
#         for sender, msg in st.session_state.chat_history[-6:]:
#             role = "User" if sender == "You" else "Bot"
#             memory_context += f"{role}: {msg}\n"

#         with st.container():
#             with st.form(key="chat_input_form", clear_on_submit=True):
#                 user_query = st.text_input("💬 Type your message", key="user_input")
#                 submitted = st.form_submit_button("Send")

#             if submitted and user_query:
#                 st.session_state.chat_history.append(("You", user_query))

#                 if "graph" in user_query.lower() or "show" in user_query.lower():
#                     st.pyplot(plot_health_trends(df))
#                     st.session_state.chat_history.append(("Sparkle Bot", "📊 Here's your health trend graph!"))
#                 else:
#                     prompt = f"{memory_context}User: {user_query}\nBot:"
#                     gemini_reply = ask_gemini(prompt, "\n".join(insights))
#                     st.session_state.pending_message = gemini_reply

#                 st.rerun()

#     except Exception as e:
#         st.error(f"🚨 Error processing your CSV: {e}")
# else:
#     st.info("👆 Please upload your health log CSV to start chatting.")

# if "chat_history" in st.session_state and st.session_state.chat_history:
#     export_text = ""
#     for sender, msg in st.session_state.chat_history:
#         emoji = "❓" if sender == "You" else "🔍"
#         export_text += f"{emoji} {msg}\n\n"

#     st.download_button(
#         label="📥 Download Chat (.txt)",
#         data=export_text,
#         file_name="sparkle_chat.txt",
#         mime="text/plain"
#     )









# import streamlit as st
# import requests
# import json
# from dotenv import load_dotenv
# import os
# import time

# # Load the API key from .env file
# load_dotenv()
# GEMINI_API_KEY = "AIzaSyBn3LmJbLYp_BypnA2eSd5YC2kim3wlUWo"

# # Function to handle requests to the Gemini API for the chatbot response
# def ask_gemini(user_message):
#     url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={GEMINI_API_KEY}"

#     prompt = f"""
# You are Sparkle, an AI health coach. Your role is to assist with health-related queries.
# User's question: {user_message}
# You must respond in a friendly, supportive, and intelligent way.
# """

#     headers = {"Content-Type": "application/json"}
#     data = {
#         "contents": [
#             {
#                 "parts": [{"text": prompt}]
#             }
#         ]
#     }

#     try:
#         response = requests.post(url, headers=headers, data=json.dumps(data))
#         response.raise_for_status()
#         gemini_reply = response.json()["candidates"][0]["content"]["parts"][0]["text"]
#         return gemini_reply
#     except Exception as e:
#         return f"⚠️ Gemini API error: {e}"

# # Streamlit UI for the chatbot
# st.set_page_config(page_title="Sparkle AI Health Chatbot", layout="centered")
# st.title("🤖 Sparkle: AI Health Chatbot")
# st.caption("Chat with Sparkle about health, wellness, healthcare, health products, and more.")

# # Initialize the session state for chat history and pending message
# if "chat_history" not in st.session_state:
#     st.session_state.chat_history = []
# if "pending_message" not in st.session_state:
#     st.session_state.pending_message = None

# # Display chat interface
# with st.container():
#     st.markdown("### 🗨️ Health Chat")
#     chat_area = st.container()
#     with chat_area:
#         for sender, msg in st.session_state.chat_history:
#             emoji = "❓" if sender == "You" else "🔍"
#             with st.chat_message(emoji):
#                 st.markdown(msg)

#         if st.session_state.pending_message:
#             with st.chat_message("🔍"):
#                 with st.spinner("Sparkle is thinking..."):
#                     time.sleep(1.5)
#                     st.markdown(st.session_state.pending_message)
#             st.session_state.chat_history.append(("Sparkle Bot", st.session_state.pending_message))
#             st.session_state.pending_message = None
#             st.rerun()

# # Input field for user message
# with st.container():
#     with st.form(key="chat_input_form", clear_on_submit=True):
#         user_query = st.text_input("💬 Type your message", key="user_input")
#         submitted = st.form_submit_button("Send")

#     if submitted and user_query:
#         st.session_state.chat_history.append(("You", user_query))

#         # Handle health-related queries
#         health_keywords = ["health", "wellness", "healthcare", "medicine", "nutrition", "fitness", "health products", "hospitals", "doctors", "medications"]
#         if any(keyword in user_query.lower() for keyword in health_keywords):
#             # If the query contains health-related keywords, respond using Gemini API
#             prompt = f"User: {user_query}\nBot:"
#             gemini_reply = ask_gemini(prompt)
#             st.session_state.pending_message = gemini_reply
#         else:
#             # If the query is not health-related, respond with a default message
#             st.session_state.pending_message = "⚠️ Sorry, I can only assist with health-related queries. Please ask about health topics."

#         st.rerun()

# # Allow downloading the chat history as a text file
# if "chat_history" in st.session_state and st.session_state.chat_history:
#     export_text = ""
#     for sender, msg in st.session_state.chat_history:
#         emoji = "❓" if sender == "You" else "🔍"
#         export_text += f"{emoji} {msg}\n\n"

#     st.download_button(
#         label="📥 Download Chat (.txt)",
#         data=export_text,
#         file_name="sparkle_chat.txt",
#         mime="text/plain"
#     )

# # Function to create a PDF from the chat history
# from fpdf import FPDF
# import io

# def create_chat_pdf(chat_history):
#     pdf = FPDF()
#     pdf.add_page()
#     pdf.set_font("Arial", size=12)

#     for sender, msg in chat_history:
#         emoji = "❓" if sender == "You" else "🔍"
#         text = f"{emoji} {msg}"
#         pdf.multi_cell(0, 10, txt=text)
#         pdf.ln()

#     pdf_buffer = io.BytesIO()
#     pdf.output(pdf_buffer)
#     return pdf_buffer.getvalue()

# # Allow downloading the chat history as a PDF
# if st.button("📄 Download Chat (.pdf)"):
#     pdf_bytes = create_chat_pdf(st.session_state.chat_history)
#     st.download_button(
#         label="📥 Save Chat PDF",
#         data=pdf_bytes,
#         file_name="sparkle_chat.pdf",
#         mime="application/pdf"
#     )

# import streamlit as st
# import requests
# import json
# from dotenv import load_dotenv
# import os
# import time

# # Load the API key from .env file
# load_dotenv()
# GEMINI_API_KEY = "AIzaSyBn3LmJbLYp_BypnA2eSd5YC2kim3wlUWo"

# # Function to handle requests to the Gemini API for the chatbot response
# def ask_gemini(user_message):
#     url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={GEMINI_API_KEY}"

#     prompt = f"""
# You are Sparkle, an AI health coach. Your role is to assist users with health-related queries in a friendly, supportive, and intelligent way.

# You are capable of providing personalized guidance and educational support on:

# 🛌 Sleep & Rest:
# - Sleep habits and how to improve sleep quality
# - Sleep hygiene and routines

# 💧 Hydration & Nutrition:
# - Water intake goals and hydration habits
# - Macronutrients (carbs, protein, fats) explained in simple terms
# - Meal planning tips (e.g., diabetic-friendly, low-carb, heart-healthy)
# - Sample healthy food or snack ideas

# 🏃 Physical Activity & Health Goals:
# - Daily step count tracking
# - Personalized fitness suggestions
# - Health goal tracking (e.g., “I want to walk 10,000 steps a day”)
# - Safe exercise and injury prevention

# 🙂 Mood & Mental Well-being:
# - Mood tracking and emotional patterns
# - Stress management tips
# - Breathing exercises and mindfulness practices
# - Recognizing signs of burnout and self-care suggestions

# 🧪 Medical Literacy (non-diagnostic):
# - Common medications (tablets, syrups, powders, injections, insulins, etc.)
# - Medical devices and their usage (e.g., glucometers, BP monitors)
# - Founders or inventors of medical breakthroughs or pharma companies
# - Differences between generic and branded medicines
# - Basics of lab tests and their interpretations (e.g., HbA1c, BMI)
# - Awareness of chronic conditions like diabetes or hypertension
# - Public health topics like vaccines, disease prevention, first aid

# 📱 Health-Tech & Modern Care:
# - Digital health innovations (e.g., wearables, smart health apps)
# - AI in healthcare and robotic diagnostics
# - Benefits of telemedicine

# 🌿 Environmental & Holistic Wellness:
# - Benefits of sunlight, walking, and green spaces
# - Effects of pollution on respiratory health
# - Digital detox and reducing screen time

# 💡 If the user asks about **personal health insights** (e.g., “How am I doing?”, “Show my weekly summary”), and no health data has been provided yet, kindly inform them to upload or generate their insights first.

# ❌ If the user's query is **not related to health, wellness, medicine, or the medical industry**, politely let them know that you are only trained to handle health-related topics and suggest they ask something in that area.

# Always personalize your responses based on the user’s intent and the available insights. Be empathetic, motivational, and avoid generic replies. Your tone should be encouraging and human-like, just like a friendly wellness coach.

# User's question: {user_message}

# """

#     headers = {"Content-Type": "application/json"}
#     data = {
#         "contents": [
#             {
#                 "parts": [{"text": prompt}]
#             }
#         ]
#     }

#     try:
#         response = requests.post(url, headers=headers, data=json.dumps(data))
#         response.raise_for_status()
#         gemini_reply = response.json()["candidates"][0]["content"]["parts"][0]["text"]
#         return gemini_reply
#     except Exception as e:
#         return f"⚠️ Gemini API error: {e}"

# # Streamlit UI for the chatbot
# st.set_page_config(page_title="Sparkle AI Health Chatbot", layout="centered")
# st.title("🤖 Sparkle: AI Health Chatbot")
# st.caption("Chat with Sparkle about health, wellness, healthcare, health products, and more.")

# # Initialize the session state for chat history and pending message
# if "chat_history" not in st.session_state:
#     st.session_state.chat_history = []
# if "pending_message" not in st.session_state:
#     st.session_state.pending_message = None

# # Display chat interface
# with st.container():
#     st.markdown("### 🗨️ Health Chat")
#     chat_area = st.container()
#     with chat_area:
#         for sender, msg in st.session_state.chat_history:
#             emoji = "❓" if sender == "You" else "🔍"
#             with st.chat_message(emoji):
#                 st.markdown(msg)

#         if st.session_state.pending_message:
#             with st.chat_message("🔍"):
#                 with st.spinner("Sparkle is thinking..."):
#                     time.sleep(1.5)
#                     st.markdown(st.session_state.pending_message)
#             st.session_state.chat_history.append(("Sparkle Bot", st.session_state.pending_message))
#             st.session_state.pending_message = None
#             st.rerun()

# # Input field for user message
# with st.container():
#     with st.form(key="chat_input_form", clear_on_submit=True):
#         user_query = st.text_input("💬 Type your message", key="user_input")
#         submitted = st.form_submit_button("Send")

#     if submitted and user_query:
#         st.session_state.chat_history.append(("You", user_query))

#         # Handle all messages, no health-related condition
#         prompt = f"User: {user_query}\nBot:"
#         gemini_reply = ask_gemini(prompt)
#         st.session_state.pending_message = gemini_reply

#         st.rerun()

# # Allow downloading the chat history as a text file
# if "chat_history" in st.session_state and st.session_state.chat_history:
#     export_text = ""
#     for sender, msg in st.session_state.chat_history:
#         emoji = "❓" if sender == "You" else "🔍"
#         export_text += f"{emoji} {msg}\n\n"

#     st.download_button(
#         label="📥 Download Chat (.txt)",
#         data=export_text,
#         file_name="sparkle_chat.txt",
#         mime="text/plain"
#     )



# streamlit run streamlit_chatbot.py
# https://platform.openai.com/api-keys
# import streamlit as st
# import requests
# import json
# from dotenv import load_dotenv
# import os
# import time

# # Load the API key from .env file
# load_dotenv()
# GEMINI_API_KEY = "AIzaSyBn3LmJbLYp_BypnA2eSd5YC2kim3wlUWo"

# # Flask backend endpoint
# INSIGHT_API_URL = "http://localhost:10000/upload-csv/"

# # Function to get Gemini response
# def ask_gemini(user_message):
#     url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={GEMINI_API_KEY}"

#     prompt = f"""
# You are Sparkle, an AI health coach. Your role is to assist users with health-related queries in a friendly, supportive, and intelligent way.

# If the user asks for their personal insights, and no data has been provided yet, kindly inform them to upload or generate their health insights first.

# User's question: {user_message}

# """

#     headers = {"Content-Type": "application/json"}
#     data = {
#         "contents": [
#             {
#                 "parts": [{"text": prompt}]
#             }
#         ]
#     }

#     try:
#         response = requests.post(url, headers=headers, data=json.dumps(data))
#         response.raise_for_status()
#         gemini_reply = response.json()["candidates"][0]["content"]["parts"][0]["text"]
#         return gemini_reply
#     except Exception as e:
#         return f"⚠️ Gemini API error: {e}"

# # Function to fetch insights from Flask backend
# def fetch_insights_from_backend():
#     try:
#         response = requests.post(INSIGHT_API_URL, timeout=10)
#         response.raise_for_status()
#         data = response.json()
#         return data.get("insights", "No insights available.")
#     except Exception as e:
#         return f"⚠️ Could not retrieve insights: {e}"

# # Streamlit App Configuration
# st.set_page_config(page_title="Sparkle AI Health Chatbot", layout="centered")
# st.title("🤖 Sparkle: AI Health Chatbot")
# st.caption("Chat with Sparkle about health, wellness, and your weekly insights.")

# # Chat history state
# if "chat_history" not in st.session_state:
#     st.session_state.chat_history = []
# if "pending_message" not in st.session_state:
#     st.session_state.pending_message = None

# # Chat message UI
# with st.container():
#     st.markdown("### 🗨️ Health Chat")
#     chat_area = st.container()
#     with chat_area:
#         for sender, msg in st.session_state.chat_history:
#             emoji = "❓" if sender == "You" else "🔍"
#             with st.chat_message(emoji):
#                 st.markdown(msg)

#         if st.session_state.pending_message:
#             with st.chat_message("🔍"):
#                 with st.spinner("Sparkle is thinking..."):
#                     time.sleep(1.5)
#                     st.markdown(st.session_state.pending_message)
#             st.session_state.chat_history.append(("Sparkle Bot", st.session_state.pending_message))
#             st.session_state.pending_message = None
#             st.rerun()

# # User input form
# with st.container():
#     with st.form(key="chat_input_form", clear_on_submit=True):
#         user_query = st.text_input("💬 Type your message", key="user_input")
#         submitted = st.form_submit_button("Send")

#     if submitted and user_query:
#         st.session_state.chat_history.append(("You", user_query))

#         # Detect health insight queries
#         if "how am i doing" in user_query.lower() or "weekly insight" in user_query.lower():
#             insight_text = fetch_insights_from_backend()
#             st.session_state.pending_message = f"📊 Here's your weekly insight:\n\n{insight_text}"
#         else:
#             gemini_reply = ask_gemini(user_query)
#             st.session_state.pending_message = gemini_reply

#         st.rerun()

# # Export chat history
# if "chat_history" in st.session_state and st.session_state.chat_history:
#     export_text = ""
#     for sender, msg in st.session_state.chat_history:
#         emoji = "❓" if sender == "You" else "🔍"
#         export_text += f"{emoji} {msg}\n\n"

#     st.download_button(
#         label="📥 Download Chat (.txt)",
#         data=export_text,
#         file_name="sparkle_chat.txt",
#         mime="text/plain"
#     )
