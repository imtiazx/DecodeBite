# Dependencies
import streamlit as st
import requests
from typing import Optional
import base64
from together import Together
import json

# Load environment vairables
TOGETHER_API_KEY = st.secrets["TOGETHER_API_KEY"]
LANGFLOW_TOKEN_ANALYSIS = st.secrets["LANGFLOW_TOKEN_ANALYSIS"]
LANGFLOW_TOKEN_CHAT = st.secrets["LANGFLOW_TOKEN_CHAT"]

# Constants
BASE_API_URL = "https://api.langflow.astra.datastax.com"
LANGFLOW_ID = "d2b3e98e-4aae-4715-8695-f50c9ae8cf50"

# Set page configuration
st.set_page_config(layout="wide", page_title="DecodeBite", page_icon="🍎")

# Sidebar navigation
sidebar_options = ["Home", "Upload & Extract", "Analyze & Decode"]
selected_option = st.sidebar.radio("Select a step", sidebar_options)

# Initialize session state
if "uploaded_image" not in st.session_state:
    st.session_state.uploaded_image = None
if "extracted_info" not in st.session_state:
    st.session_state.extracted_info = ""
if "final_text" not in st.session_state:
    st.session_state.final_text = ""
if "analysis_report" not in st.session_state:
    st.session_state.analysis_report = {}
if "ai_response" not in st.session_state:
    st.session_state.ai_response = ""

# Function to encode an image to Base64
def encode_image(image_file):
    try:
        image_file.seek(0)
        return base64.b64encode(image_file.read()).decode("utf-8")
    except Exception as e:
        st.error(f"Error encoding image: {str(e)}")
        return None
    
def run_analysis_flow(message: str,
  output_type: str = "chat",
  input_type: str = "chat",
  tweaks: Optional[dict] = None,
  application_token: Optional[str] = None) -> dict:

    api_url = f"{BASE_API_URL}/lf/{LANGFLOW_ID}/api/v1/run/food_analysis"

    payload = {
        "input_value": message,
        "output_type": output_type,
        "input_type": input_type,
    }
    headers = None
    if tweaks:
        payload["tweaks"] = tweaks
    if application_token:
        headers = {"Authorization": "Bearer " + application_token, "Content-Type": "application/json"}

    try:
        response = requests.post(api_url, json=payload, headers=headers, timeout=50)

        # Handle non-successful responses
        if response.status_code != 200:
            st.error(f"Error from API: {response.status_code}")
            return None

        # Parse and extract response text
        response_data = response.json()
        try:
            result_text = response_data["outputs"][0]["outputs"][0]["results"]["text"]["data"]["text"]
            return result_text
        except (KeyError, IndexError, TypeError) as e:
            st.error(f"Error parsing AI response: {e}")
            return None
    except requests.RequestException as e:
        st.error(f"Request Exception: {e}")
        return None
    
def generate_analysis(extracted_info):
    TWEAKS = {
    "TextInput-NDzDD": {
        "input_value": "extracted_info"
    },
    }
    result = run_analysis_flow(extracted_info, tweaks=TWEAKS, application_token=LANGFLOW_TOKEN_ANALYSIS)
    return result

# Function to convert dictionary to a displayable string
def dict_to_string(obj, level=0):
    strings = []
    indent = "  " * level
    if isinstance(obj, dict):
        for key, value in obj.items():
            if isinstance(value, (dict, list)):
                nested_string = dict_to_string(value, level + 1)
                strings.append(f"{indent}{key}: {nested_string}")
            else:
                strings.append(f"{indent}{key}: {value}")
    elif isinstance(obj, list):
        for idx, item in enumerate(obj):
            nested_string = dict_to_string(item, level + 1)
            strings.append(f"{indent}Item {idx + 1}: {nested_string}")
    else:
        strings.append(f"{indent}{obj}")
    return ", ".join(strings)

# Function to run the Langflow flow
def run_chat_flow(message: str, output_type: str = "chat", input_type: str = "chat",
             tweaks: Optional[dict] = None, application_token: Optional[str] = None) -> Optional[str]:
    api_url = f"{BASE_API_URL}/lf/{LANGFLOW_ID}/api/v1/run/chat"
    payload = {
        "input_value": message,
        "output_type": output_type,
        "input_type": input_type
    }
    if tweaks:
        payload["tweaks"] = tweaks

    headers = {
        "Authorization": f"Bearer {application_token}",
        "Content-Type": "application/json"
    } if application_token else None

    try:
        response = requests.post(api_url, json=payload, headers=headers, timeout=50)

        # Handle non-successful responses
        if response.status_code != 200:
            st.error(f"Error from API: {response.status_code}")
            return None

        # Parse and extract response text
        response_data = response.json()
        try:
            result_text = response_data["outputs"][0]["outputs"][0]["results"]["text"]["data"]["text"]
            return result_text
        except (KeyError, IndexError, TypeError) as e:
            st.error(f"Error parsing AI response: {e}")
            return None
    except requests.RequestException as e:
        st.error(f"Request Exception: {e}")
        return None
    
# Function to generate AI response
def ask_ai_func():
    st.subheader("Chat to Decode")

    # Display "Sample Questions" below the header
    st.markdown("<h3 style='font-size: 16px;'>Sample Questions</h3>", unsafe_allow_html=True)

    sample_questions = """
    <ol>
        <li>What is the recommended average daily intake (ADI) for sodium benzoate, and what are its primary functional uses in food?</li>
        <li>Why is citric acid (acidity regulator 330) commonly used in food products?</li>
        <li>How do saturated and unsaturated fatty acids differ in structure and health effects?</li>
        <li>What are the potential effects of consuming 50 grams of sodium at once?</li>
        <li>What is bone phosphate, and why is it permitted for use in food products?</li>
    </ol>
    """
    st.markdown(f"<div style='border: 1px solid #ddd; padding: 10px; border-radius: 5px;'>{sample_questions}</div>", unsafe_allow_html=True)

    user_question = st.text_input("Ask a question:")

    # Retrieve stored AI response from session state, if available
    ai_response = st.session_state.get('ai_response', None)


    if st.button("Ask AI"):
        with st.spinner("Waiting for AI to respond..."):
            tweaks = {"TextInput-6CQcN": {"input_value": user_question}}
            response = run_chat_flow(
                "",
                tweaks=tweaks,
                application_token=LANGFLOW_TOKEN_CHAT
            )
            if response:
                # Store the AI response in session state to persist it across sections
                st.session_state.ai_response = response
                response_box = f"""
                <div style='border: 1px solid #ddd; padding: 10px; border-radius: 5px; margin-top: 10px;'>
                    <h3 style='text-align: center; margin: 0;'>AI Response</h3>
                    <p>{response}</p>
                </div>
                """
                st.markdown(response_box, unsafe_allow_html=True)
            else:
                st.error("No valid response received from AI.")

    if ai_response:
        st.markdown(f"<div style='border: 1px solid #ddd; padding: 10px; border-radius: 5px; margin-top: 10px;'><h3 style='text-align: center; margin: 0;'>AI Response</h3><p>{ai_response}</p></div>", unsafe_allow_html=True)

# Home section
if selected_option == "Home":
    st.title("Welcome to DecodeBite!")
    st.markdown("""
        🌍 The global packaged food market is worth an estimated **$5.32 trillion USD**, with a projected **6.2% CAGR**.  
        🍽️ Over **5,000 substances** are added to our food, altering color, texture, flavor, and more!
    """)
    st.subheader("Our Solution:")
    st.markdown("""
        1. **Upload an Image** of the ingredient label from your food packaging.  
        2. **Extract Information** from the image for a detailed analysis.  
        3. **Edit and Finalize** the extracted text.  
        4. **Review** the finalized information in the "Analyze & Decode" section.
    """)

# Upload & Extract section
if selected_option == "Upload & Extract":
    st.header("Upload & Extract")
    uploaded_image = st.file_uploader("NOTE: Please refresh the page if you want to upload a new image.", type=["jpg", "png", "jpeg"])
    if uploaded_image:
        st.session_state.uploaded_image = uploaded_image
        st.success("Progress: Image uploaded successfully.")
        base64_image = encode_image(uploaded_image)
        if not st.session_state.extracted_info and base64_image:
            try:
                client = Together()
                stream = client.chat.completions.create(
                    model="meta-llama/Llama-3.2-11B-Vision-Instruct-Turbo",
                    messages=[
                        {"role": "user", "content": [
                            {"type": "text", "text": "Extract and format text information from the image into a structured, readable format. Ensure proper alignment, spacing, and logical grouping of content."},
                            {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}}
                        ]}
                    ],
                    stream=True,
                )
                extracted_text = ""
                for chunk in stream:
                    if hasattr(chunk, "choices") and chunk.choices:
                        choice = chunk.choices[0]
                        if hasattr(choice, "delta") and hasattr(choice.delta, "content"):
                            extracted_text += choice.delta.content
                if extracted_text.strip():
                    st.session_state.extracted_info = extracted_text
                    st.success("Progress: Information extracted successfully!")
                else:
                    st.error("No content received from the AI.")
            except Exception as e:
                st.error(f"Error during image processing: {str(e)}")
    if st.session_state.uploaded_image and st.session_state.extracted_info:
        col1, col2 = st.columns(2)
        with col1:
            st.image(st.session_state.uploaded_image, caption="Uploaded Image", use_container_width=True)
        with col2:
            st.session_state.final_text = st.text_area("Edit Extracted Information", st.session_state.extracted_info, height=400)

# Analyze & Decode section
if selected_option == "Analyze & Decode":
    st.markdown("<h2 style='font-size: 24px;'>Extracted Text</h2>", unsafe_allow_html=True)
    if st.session_state.final_text.strip():
        st.markdown(f"<div style='border: 1px solid #ddd; padding: 10px; border-radius: 5px;'><p>{st.session_state.final_text}</p></div>", unsafe_allow_html=True)
    else:
        st.info("No information available. Please extract and edit the text in the 'Upload & Extract' section.")
    if st.button("Generate Analysis"):
        with st.spinner("Generating analysis... Please wait..."):
            if st.session_state.extracted_info.strip():
                analysis_report = generate_analysis(st.session_state.extracted_info)
                try:
                    analysis_dict = json.loads(analysis_report)
                    st.session_state.analysis_report = analysis_dict
                except json.JSONDecodeError as e:
                    st.error(f"Error parsing analysis report: {e}")
            else:
                st.error("No extracted information available. Please upload an image and extract the text first.")
    st.markdown("<h2 style='font-size: 24px;'>Analysis Report by Generative AI</h2>", unsafe_allow_html=True)
    if st.session_state.analysis_report:
        categories = ["High Risk Ingredients", "Cautionary Ingredients", "Safe Consumption Insights"]
        for category in categories:
            if category in st.session_state.analysis_report:
                content = dict_to_string(st.session_state.analysis_report[category])
                st.markdown(f"<div style='border: 1px solid #ddd; padding: 10px; border-radius: 5px;'><h3 style='text-align: center; margin: 0;'>{category}</h3><p>{content}</p></div>", unsafe_allow_html=True)
                st.markdown("<br>", unsafe_allow_html=True)

    # Disclaimer in italic text after the analysis boxes
    st.markdown("<i><strong>Disclaimer:</strong> This analysis is generated by an LLM. Please review with subject matter experts. To analyze a new image, please refresh the webpage.</i>", unsafe_allow_html=True)

    # "Chat to Decode" section
    ask_ai_func()