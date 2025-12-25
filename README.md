# AI System Architect

**AI System Architect** is a Streamlit-based tool that uses Google's Gemini 2.5 Flash model to transform high-level application ideas into concrete technical specifications. It automates the initial phases of software design by generating module breakdowns, database schemas, SQL scripts, and core backend logic in seconds.

## Features

* **Module Decomposition:** Breaks down app ideas into distinct technical modules (JSON format).
* **Database Design:** Automatically generates a relational schema structure.
* **SQL Generation:** Writes production-ready PostgreSQL `CREATE TABLE` scripts with constraints and indexes.
* **Logic Implementation:** Drafts Python/Flask pseudo-code for the critical path of the application.
* **Direct API Integration:** Uses direct HTTP requests to Google's API, avoiding SDK dependency conflicts.
* **Exportable Reports:** Download the full technical specification as a Markdown (`.md`) file.

## Prerequisites

* **Python 3.12+**
* **Google Gemini API Key:** You need a valid API key from [Google AI Studio](https://aistudio.google.com/).

## Installation

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/AbhishekAwasthi565/AI-System-Architect.git](https://github.com/AbhishekAwasthi565/AI-System-Architect.git)
    cd ai-system-architect
    ```

2.  **Install Dependencies:**
    Run the following command to install the required libraries:
    ```bash
    pip install streamlit requests
    ```

## Configuration

1.  **API Key Setup:**
    * **Option A (Recommended):** Enter your API key directly in the application sidebar when running the app.
    * **Option B (Hardcode):** Edit the script and paste your key into the `DEFAULT_API_KEY` variable (line 6), though this is not recommended for shared code.

2.  **Model Selection:**
    * The tool defaults to `gemini-2.5-flash`. You can change the `MODEL_NAME` variable in the code if you wish to use a different version (e.g., `gemini-1.5-pro`).

## Usage

1.  **Run the Application:**
    ```bash
    streamlit run app.py
    ```

2.  **Workflow:**
    * **Sidebar:** Paste your Google API Key.
    * **Input:** Describe your application idea in the text area (e.g., *"A ride-sharing app for long-distance carpooling"*).
    * **Generate:** Click the **Generate Architecture** button.
    * **Review:** Navigate through the tabs to see the Modules, Schema, SQL, and Code.
    * **Download:** Click **Download Full Technical Spec** to save the results.

## Project Structure

```text
ai-system-architect/
│
├── app.py              # Main Streamlit application
└── README.md           # Documentation

```

## Troubleshooting

* **Error: `400 Bad Request` or `Invalid API Key**`:
* Ensure your API key is correct and has access to the Generative Language API.


* **JSON Parsing Errors**:
* Occasionally, the AI might return text outside of the JSON format. Simply click "Generate" again; the temperature setting (0.2) usually prevents this.


* **Connection Error**:
* Check your internet connection. Since this uses `requests`, no proxy configuration is handled automatically.



## License

This project is open-source. Feel free to modify and integrate it into your workflow.
