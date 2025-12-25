import streamlit as st
import requests
import json

# --- CONFIGURATION ---
DEFAULT_API_KEY = ""
MODEL_NAME = "gemini-2.5-flash"

# --- PAGE CONFIG (Must be the first Streamlit command) ---
st.set_page_config(page_title="AI Architecture Tool", page_icon="🏗️", layout="wide")


def get_gemini_response(api_key, system_role, user_prompt):
    """
    Direct HTTP call to Google Gemini API.
    Bypasses library version issues and allows full control over tokens.
    """
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL_NAME}:generateContent?key={api_key}"

    headers = {"Content-Type": "application/json"}

    # Construct Payload
    payload = {
        "contents": [{
            "parts": [{"text": f"SYSTEM ROLE: {system_role}\n\nUSER TASK: {user_prompt}"}]
        }],
        "generationConfig": {
            "temperature": 0.2,
            "maxOutputTokens": 8192  # Increased to prevent truncation
        }
    }

    try:
        response = requests.post(url, headers=headers, json=payload)

        if response.status_code != 200:
            return f"Error {response.status_code}: {response.text}"

        data = response.json()

        # Safely extract text
        if 'candidates' in data and data['candidates']:
            return data['candidates'][0]['content']['parts'][0]['text']
        else:
            return "Error: No content returned from API."

    except Exception as e:
        return f"Connection Error: {str(e)}"


# --- PROMPT TEMPLATES ---
PROMPTS = {
    "modules": """
    You are a Senior Software Architect. Analyze the user's request.
    Break it down into distinct technical modules (e.g., Auth, Payments, Tracking).
    Output Format: A clean JSON list of objects.
    Keys: "module_name", "description", "responsibilities".
    IMPORTANT: Return ONLY valid JSON. No Markdown formatting.
    """,

    "schema": """
    You are a Database Engineer. 
    Design a relational database schema based on the provided modules.
    Output Format: A clean JSON list of tables.
    Keys: "table_name", "columns" (list of objects with name, type, constraints).
    IMPORTANT: Return ONLY valid JSON. No Markdown formatting.
    """,

    "sql": """
    You are a Lead DBA. 
    Write the complete PostgreSQL CREATE TABLE scripts for the provided schema.
    - Use UUIDs for primary keys.
    - Include Foreign Key constraints.
    - Include meaningful comments.
    - Add INDEXES for performance.
    Output Format: Pure SQL code block.
    """,

    "code": """
    You are a Backend Lead. 
    Write the Python/Flask pseudo-code for the Critical Path logic (e.g., matching a user to a service).
    - Focus on the complex logic (Matching, Payment, Tracking).
    - Do not write boilerplate (like imports).
    - Handle edge cases (e.g., "No walkers found").
    Output Format: Python code block.
    """
}

# --- UI LAYOUT ---
st.title("AI System Architect")
st.markdown("### Transform High-Level Ideas into Technical Specs")

# Sidebar
with st.sidebar:
    st.header("Setup")
    api_key = st.text_input("Enter Google API Key:", value=DEFAULT_API_KEY, type="password")

    st.markdown("---")
    st.info("This tool uses **Gemini 2.5 Flash** to generate professional architectural artifacts.")
    st.markdown("Step 1: Define Modules\nStep 2: Design DB\nStep 3: Write SQL\nStep 4: Write Logic")

# Main Input Area
col1, col2 = st.columns([2, 1])
with col1:
    user_req = st.text_area(
        "Describe your application:",
        height=150,
        placeholder="E.g., I want a Tinder-style app for adopting pets. Users swipe on dogs, match with shelters, and chat..."
    )

generate_btn = st.button("Generate Architecture", type="primary")

# --- MAIN LOGIC ---
if generate_btn:
    if not api_key:
        st.error("Please enter your API Key in the sidebar.")
    elif not user_req:
        st.warning("Please describe your app idea first.")
    else:
        # Create a container for the status updates
        status_container = st.status("Architecting your solution...", expanded=True)

        try:
            # 1. Modules
            status_container.write("Analyzing requirements & defining modules...")
            modules_res = get_gemini_response(api_key, PROMPTS["modules"], user_req)
            st.session_state['modules'] = modules_res

            # 2. Schema
            status_container.write("Designing database structure...")
            schema_res = get_gemini_response(api_key, PROMPTS["schema"], modules_res)
            st.session_state['schema'] = schema_res

            # 3. SQL
            status_container.write("Writing SQL scripts...")
            sql_res = get_gemini_response(api_key, PROMPTS["sql"], schema_res)
            st.session_state['sql'] = sql_res

            # 4. Code
            status_container.write("Implementing core logic...")
            code_res = get_gemini_response(api_key, PROMPTS["code"], f"Modules: {modules_res}\nSchema: {schema_res}")
            st.session_state['code'] = code_res

            status_container.update(label="Architecture Complete!", state="complete", expanded=False)

        except Exception as e:
            st.error(f"An unexpected error occurred: {e}")

# --- DISPLAY RESULTS ---
if 'modules' in st.session_state:
    st.divider()

    # Create Tabs
    tab1, tab2, tab3, tab4 = st.tabs([
        "Modules (JSON)",
        "Data Schema (JSON)",
        "SQL Script",
        "Core Logic (Python)"
    ])

    with tab1:
        st.subheader("System Modules")
        st.code(st.session_state['modules'], language='json')

    with tab2:
        st.subheader("Database Schema Design")
        st.code(st.session_state['schema'], language='json')

    with tab3:
        st.subheader("Production SQL Script")
        st.markdown("*Ready to run in PostgreSQL/MySQL*")
        st.code(st.session_state['sql'], language='sql')

    with tab4:
        st.subheader("Backend Logic Implementation")
        st.code(st.session_state['code'], language='python')

    # Download Feature
    st.divider()
    # Corrected f-string syntax (no space after f)
    full_report = f"""# Technical Specification
    Generated by AI System Architect
    
    ## 1. System Modules
    ```json
    {st.session_state['modules']}
    {st.session_state['schema']}
    {st.session_state['sql']}
    {st.session_state['code']}
    """
    st.download_button(
        label="Download Full Technical Spec (.md)",
        data=full_report,
        file_name="technical_spec.md",
        mime="text/markdown"
    )