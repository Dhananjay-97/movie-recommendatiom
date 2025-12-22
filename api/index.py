import os
from flask import Flask, redirect, render_template, request, url_for
from openai import OpenAI

app = Flask(__name__)

# Initialize client (looks for REDACTED env var)
client = OpenAI(api_key=os.getenv("REDACTED"))

@app.route("/", methods=("GET", "POST"))
def index():
    if request.method == "POST":
        category = request.form["category"]
        number = request.form["number"]
        
        # input validation
        if not category or not number:
             return redirect(url_for("index", result="Please provide both a category and a number."))

        try:
            response = client.chat.completions.create(
                model="gpt-3.5-turbo", # Cost-effective and fast
                messages=[
                    {"role": "system", "content": "You are a helpful movie critic."},
                    {"role": "user", "content": generate_prompt(number, category)}
                ],
                temperature=0.7,
            )
            result = response.choices[0].message.content
            return redirect(url_for("index", result=result))
            
        except Exception as e:
            return redirect(url_for("index", result=f"Error: {str(e)}"))

    result = request.args.get("result")
    return render_template("index.html", result=result)

def generate_prompt(number, category):
    return f"Recommend the best {number} {category} movies to watch. Provide the list with a short 1-sentence summary for each."