from flask import Flask, render_template, request, jsonify
from openai import OpenAI
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Create Flask application
app = Flask(__name__)

# Create OpenAI client
client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)


# Home page
@app.route("/")
def home():
    return render_template("index.html")


# Generate assignment
@app.route("/generate", methods=["POST"])
def generate_assignment():

    try:

        # Get data from website
        data = request.get_json()

        topic = data.get("topic", "").strip()
        subject = data.get("subject", "").strip()
        assignment_type = data.get("assignment_type", "").strip()
        length = data.get("length", "").strip()

        # Check topic
        if not topic:

            return jsonify({
                "error": "Please enter an assignment topic."
            }), 400


        # Prompt for AI
        prompt = f"""
You are an academic writing assistant.

Create a well-structured educational assignment.

Topic: {topic}

Subject: {subject}

Assignment Type: {assignment_type}

Requested Length: {length}


Requirements:

1. Create a clear and relevant title.
2. Write a good introduction.
3. Explain the main concepts using headings.
4. Include relevant examples where useful.
5. Write a clear conclusion.
6. Use simple academic language.
7. Organize the content clearly.
8. Do not invent references or citations.
9. Make the content educational and easy to understand.
10. The assignment should be original and well structured.

Return only the assignment content.
"""


        # Send request to OpenAI
        response = client.responses.create(

            model="gpt-5.6-luna",

            input=prompt
        )


        # Get generated text
        assignment = response.output_text


        # Send result back to website
        return jsonify({

            "assignment": assignment

        })


    except Exception as error:

        print("ERROR:", error)

        return jsonify({

            "error": "Something went wrong while generating the assignment."

        }), 500


# Start application
if __name__ == "__main__":

    app.run(
        debug=True
    )