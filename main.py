from flask import Flask, render_template, request
import os

from analyzer import analyze_ads
from ai_report import generate_report

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@app.route("/", methods=["GET","POST"])
def index():

    summary = None
    report = None

    if request.method == "POST":

        file = request.files["file"]

        if file:

            path = os.path.join(UPLOAD_FOLDER, file.filename)
            file.save(path)

            summary = analyze_ads(path)

            try:
                report = generate_report(summary)
            except Exception as e:
                report = f"AI report generation failed: {str(e)}"

    return render_template(
        "index.html",
        summary=summary,
        report=report
    )

if __name__ == "__main__":
    app.run(debug=True)