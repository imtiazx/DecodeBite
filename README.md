# DecodeBite

DecodeBite helps users analyze packaged food labels by extracting ingredients and analyzing them using generative AI. The app categorizes the ingredients into potential risk levels (e.g., Low, Medium, High) and allows users to chat with AI for more information about food additives or general ingredient-related questions.

## Features

- **Ingredient Extraction**: Upload an image of a food label, and the app will extract the ingredients listed.
- **Risk Level Categorization**: The extracted ingredients are analyzed and categorized into risk levels to help users make informed decisions about the food product.
- **AI Chat**: Users can interact with AI to ask questions about food additives, ingredient safety, and general food-related queries.

## Technologies Used

- **Streamlit**: Web app framework for easy UI development.
- **OpenAI API**: Used for generative AI to analyze ingredients and provide responses to user queries.
- **Pillow**: Image processing library used to handle uploaded food label images.
- **Python-dotenv**: Manages environment variables for API keys and other settings.
- **Together**: Provides additional AI capabilities and integration.
- **Requests**: Used for making HTTP requests to APIs.

## Installation

Follow these steps to set up the project locally.

### 1. Clone the repository:
```bash
git clone https://github.com/imtiazx/DecodeBite.git