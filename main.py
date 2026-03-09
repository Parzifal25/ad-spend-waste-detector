from flask import Flask, render_template, request
import os

from analyzer import analyze_ads
from ai_report import generate_report


app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@app.route("/", methods=["GET", "POST"])
def index():

    summary = None
    report = None

    print("REQUEST METHOD:", request.method)

    if request.method == "POST":

        file = request.files.get("file")

        if not file:
            print("No file received")
            return render_template(
                "index.html",
                summary=None,
                report="No file uploaded.",
                request=request
            )

        print("Uploaded file:", file.filename)

        # Save file
        filepath = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(filepath)

        print("File saved to:", filepath)

        try:

            # Run analysis
            summary = analyze_ads(filepath)

            print("ANALYSIS RESULT:", summary)

            # Generate AI report
            report = generate_report(summary)

            print("AI REPORT GENERATED")

        except Exception as e:

            print("ERROR:", str(e))

            report = f"Processing failed: {str(e)}"

    return render_template(
        "index.html",
        summary=summary,
        report=report,
        request=request
    )


if __name__ == "__main__":
    app.run(debug=True)
