# DecodeBite

This repository contains a Streamlit application to analyze packaged food ingredients using advanced AI tools. The app allows users to upload images or labels of food ingredient lists, extracts text information using the Together API with Ollama OCR, categorizes ingredients based on potential harm, and provides answers to user queries about food additives using Multi-Query RAG.

---

## Features

1. **Upload and Extract Text**:
   - Users can upload images of packaged food ingredient labels.
   - Text is extracted using the Together API, powered by Ollama OCR.

2. **Modify Extracted Information**:
   - Users can review and edit the extracted text for accuracy.

3. **Categorize Ingredients**:
   - Uses GPT-4o Mini to categorize ingredients based on potential harm due to overconsumption.

4. **Food Additive Queries**:
   - Employs Multi-Query RAG to answer user questions about food additives, referencing over 100+ additives.
   - Uses a custom PDF (`data.pdf`) for contextual information about additives.

---

## File Structure

- `main.py`: The main application file containing the Streamlit app code.
- `requirements.txt`: Specifies all required Python packages for the application.
- `data.pdf`: A custom PDF used for contextual references in the RAG system.

---

## Setup and Usage

### Prerequisites
- Python 3.8 or higher
- A Streamlit Cloud account for deployment (optional)
- API keys for Together API and GPT-4o Mini

### Installation
1. Clone this repository:
   ```bash
   git clone https://github.com/imtiazx/DecodeBite.git
   cd DecodeBite
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Add the required secrets in `.streamlit/secrets.toml`:
   ```toml
   TOGETHER_API_KEY = "your-together-api-key"
   LANGFLOW_TOKEN_ANALYSIS = "your-langflow-token-analysis-key"
   LANGFLOW_TOKEN_CHAT = "your-langflow-token-chat-key"
   ```

4. Place `data.pdf` in the project root.

### Run Locally
Run the app locally using the following command:
```bash
streamlit run main.py
```

### Deploy on Streamlit Cloud
1. Push the repository to GitHub.
2. Go to [Streamlit Cloud](https://streamlit.io/) and connect your repository.
3. Add your secrets under **App Settings** > **Secrets** in the Streamlit Cloud dashboard.
4. Deploy the app and share the link!

---

## Contributing

Contributions are welcome! Feel free to open issues or submit pull requests.
