import streamlit as st
import requests
import pandas as pd
from constants import MARKDOWN_DOC_STRING
from database import get_all_extractions, get_extraction_by_id

# FastAPI backend URL
fastapi_url = "http://localhost:8000"

st.markdown("""
    <style>
    /* Style the sidebar buttons */
    .sidebar .sidebar-content {
        display: flex;
        flex-direction: column;
    }

    /* Target buttons in the sidebar using data-testid */
    [data-testid="stSidebar"] [data-testid="stBaseButton-secondary"] {
        width: 100%;
    }
    """, unsafe_allow_html=True)

if "selected_section" not in st.session_state:
    st.session_state.selected_section = "API Documentation" 
st.title("Data Extraction and Query App")


# Sidebar Navigation
st.sidebar.header("Navigation")
pdf_extraction_button = st.sidebar.button("PDF Extraction", key="pdf_extraction")
url_extraction_button = st.sidebar.button("URL Extraction", key="url_extraction")
Chat_using_words = st.sidebar.button("Chat", key="chat_with_ai")
view_data = st.sidebar.button("View Data", key="view_data")
api_docs_button = st.sidebar.button("API Documentation", key="api_docs")

# Set the selected section based on button clicks
if pdf_extraction_button:
    st.session_state.selected_section = "PDF Extraction"
elif url_extraction_button:
    st.session_state.selected_section = "URL Extraction"
elif Chat_using_words:
    st.session_state.selected_section = "Chat"
elif api_docs_button:
    st.session_state.selected_section = "API Documentation"
elif view_data:
    st.session_state.selected_section = "View Data"


# Create the function to display the data table with filtering
def display_extraction_data():
    st.header("View Extracted Data")
    data = get_all_extractions()
    df = pd.DataFrame(data, columns=["ID", "Extracted Content", "Type of Extraction"])
    filter_type = st.radio("Filter by:", ("All", "ID", "Type of Extraction"))

    if filter_type == "ID":
        extraction_id = st.text_input("Enter Extraction ID")
        if extraction_id:
            filtered_data = get_extraction_by_id(extraction_id)
            if filtered_data:
                df = pd.DataFrame([filtered_data], columns=["ID", "Extracted Content", "Type of Extraction"])
            else:
                st.error("No data found with the provided ID.")
    elif filter_type == "Type of Extraction":
        extraction_type = st.text_input("Enter Type of Extraction")
        if extraction_type:
            filtered_data = df[df["Type of Extraction"].str.contains(extraction_type, case=False, na=False)]
            if not filtered_data.empty:
                df = filtered_data
            else:
                st.error("No data found for the provided extraction type.")

    if not df.empty:
        st.write(f"Showing {len(df)} records")
        st.dataframe(df, height=500, use_container_width=True)
    else:
        st.warning("No data available.")


# Display the content based on the selected section
if st.session_state.selected_section == "PDF Extraction":
    st.subheader("PDF Document Extraction")
    uploaded_pdf = st.file_uploader("Upload a PDF file", type=["pdf"])

    if uploaded_pdf is not None:
        if st.button("Extract PDF Content"):
            with st.spinner('Extracting PDF content...'):
                files = {"file": uploaded_pdf.getvalue()}
                response = requests.post(f"{fastapi_url}/process_pdf/", files={"file": uploaded_pdf})
                
                if response.status_code == 200:
                    st.success("PDF content processed successfully and saved to DB!")
                    st.text("API Response")
                    st.write(response.json())
                else:
                    st.error(f"Failed to process PDF content. Status code: {response.status_code}")

elif st.session_state.selected_section == "URL Extraction":
    st.subheader("Web URL Content Extraction")
    url_input = st.text_input("Enter a URL to extract content")

    if st.button("Extract URL Content"):
        with st.spinner('Extracting URL content...'):
            response = requests.post(f"{fastapi_url}/process_url/", json={"url": url_input})
            
            if response.status_code == 200:
                st.success("URL content processed successfully and saved to DB!")
                st.write(response.json())
            else:
                st.error(f"Failed to process URL content. Status code: {response.status_code}")

elif st.session_state.selected_section == "Chat":
    st.subheader("Chat using words")
    if "messages" not in st.session_state:
        st.session_state.messages = []

    col1, col2, col3 = st.columns([1, 3, 1])

    with col1:
        chat_id = st.text_input("Chat ID", placeholder="Enter Chat ID", key="chat_id")
    with col2:
        user_query = st.text_input("Ask a question using words", placeholder="Type your word here...", key="user_query")
    with col3:
        st.markdown("""
            <style>
            .stButton>button {
                height: 2.5em;  /* Adjust height to align with input boxes */
                line-height: 2.5em;
                margin-top: 0.7em;  /* Adjust this value to move the button down */
            }
            </style>
        """, unsafe_allow_html=True)
        send_button = st.button("Send", key="send_button")

    if send_button and user_query and chat_id:
        with st.spinner('Generating chatbot response...'):
            response = requests.post(f"{fastapi_url}/chat/", json={"id": chat_id, "question": user_query})

            if response.status_code == 200:
                ai_response = response.json().get("response", "No response available")
                st.session_state.messages.append({"role": "ai", "content": ai_response})
                st.session_state.messages.append({"role": "user", "content": user_query})
                st.success("Chatbot response generated!")
            else:
                st.error(f"Failed to generate chatbot response. Status code: {response.status_code}")

    # Display chat history below
    for message_data in reversed(st.session_state.messages):
        if message_data["role"] == "user":
            st.markdown(f"<div style='text-align: right;'><b>User:</b> {message_data['content']}</div>", unsafe_allow_html=True)
        else:
            st.markdown(f"<div style='text-align: left; width: 70%;'><b>Response:</b> {message_data['content']}</div>", unsafe_allow_html=True)

    # Call the function to display the data and filters
elif st.session_state.selected_section == "View Data":
    display_extraction_data()

elif st.session_state.selected_section == "API Documentation":
    st.markdown(MARKDOWN_DOC_STRING)