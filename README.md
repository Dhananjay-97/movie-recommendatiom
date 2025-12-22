# 🎬 AI Movie Recommender

A GenAI-powered application that recommends movies based on category, genre, or mood using OpenAI's GPT models. Built with Flask and deployed on Vercel.

## Features
- **Smart Recommendations:** Uses GPT-3.5-Turbo to understand nuance (e.g., "Sad movies from the 90s that end happily").
- **Customizable:** Choose the specific number of recommendations.
- **Serverless:** Runs entirely on Vercel functions.

## Prerequisites
1.  **OpenAI API Key**: You need an account at [platform.openai.com](https://platform.openai.com).
2.  **Python 3.9+** installed locally.

## 🚀 Running Locally

Follow these steps to get the app running on your machine:

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/dhananjaylab-movie-recommendatiom.git
    cd dhananjaylab-movie-recommendatiom
    ```

2.  **Set up Environment Variables:**
    Create a `.env` file in the root directory:
    ```bash
    # Mac/Linux
    touch .env
    ```
    Add your API key inside `.env`:
    ```text
    REDACTED=sk-your-actual-api-key-here
    FLASK_ENV=development
    ```

3.  **Install Dependencies:**
    It is recommended to use a virtual environment.
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use: venv\Scripts\activate
    pip install -r requirements.txt
    ```

4.  **Run the Application:**
    ```bash
    flask --app api/index run
    ```

5.  **Open in Browser:**
    Navigate to `http://127.0.0.1:5000`.

## ☁️ Deployment (Vercel)

1.  Install Vercel CLI: `npm i -g vercel`
2.  Run `vercel login`
3.  Run `vercel` in the project root.
4.  **Important:** When asked for Environment Variables in the Vercel dashboard, add `REDACTED` with your key value.

## Project Structure
```text
├── api/
│   ├── index.py           # Main Flask Application
│   ├── static/            # CSS and Images
│   └── templates/         # HTML Files
├── requirements.txt       # Python dependencies
└── vercel.json           # Deployment configuration