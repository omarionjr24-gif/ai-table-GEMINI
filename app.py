import streamlit as st
import pandas as pd
import google.generativeai as genai

st.set_page_config(page_title="AI Table Chatbot - Gemini", page_icon="🧠", layout="wide")

st.title("🧠 AI Table Query Chatbot")
st.caption("Powered by Google Gemini (Free)")

# ====================== API KEY ======================
if "GEMINI_API_KEY" not in st.secrets:
    st.error("❌ GEMINI_API_KEY not found in Secrets. Please add it.")
    st.stop()

genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

# ====================== FILE UPLOAD ======================
st.sidebar.header("📁 Upload Data")
uploaded_file = st.sidebar.file_uploader("CSV or Excel file", type=["csv", "xlsx", "xls"])

if uploaded_file:
    try:
        if uploaded_file.name.endswith(".csv"):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)
        
        st.success(f"✅ Loaded: {len(df)} rows × {len(df.columns)} columns")
        
        with st.expander("📊 Preview Data"):
            st.dataframe(df.head(10))
        
        # Chat
        if "messages" not in st.session_state:
            st.session_state.messages = [{"role": "assistant", "content": "Table loaded! Ask me anything about your data."}]
        
        for msg in st.session_state.messages:
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])
        
        if prompt := st.chat_input("E.g. What is the average of mathematics?"):
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)
            
            with st.chat_message("assistant"):
                with st.spinner("Analyzing..."):
                    model = genai.GenerativeModel("gemini-2.0-flash")
                    
                    data_info = f"""
                    Dataset Information:
                    - Columns: {list(df.columns)}
                    - Number of rows: {len(df)}
                    - First 5 rows: 
                    {df.head().to_string()}
                    """
                    
                    response = model.generate_content(f"{data_info}\n\nQuestion: {prompt}\nAnswer accurately and use tables if needed.")
                    answer = response.text
                    
                    st.markdown(answer)
                    st.session_state.messages.append({"role": "assistant", "content": answer})
                    
    except Exception as e:
        st.error(f"Error reading file: {e}")
else:
    st.info("👈 Upload your CLASS...S2026.xlsx file from the sidebar")
