import os
import time

from google import genai
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key=API_KEY)


def generate_report(summary):

    campaign_details = "\n".join(
        [f"{c['campaign']} : ₹{c['waste']}" for c in summary["campaign_waste"]]
    )

    issues_list = "\n".join(summary["issues"])

    prompt = f"""
    You are a digital marketing performance auditor.

    Total Spend: ₹{summary['total_spend']}
    Estimated Wasted Spend: ₹{summary['wasted_spend']}
    Waste Percentage: {summary['waste_percent']}%
    Waste Score: {summary['waste_score']}/100

    Top Waste Campaigns:
    {campaign_details}

    Detected Issues:
    {issues_list}

    Provide:
    1. Waste Summary
    2. Top 3 Waste Sources
    3. Quick Fixes
    4. Estimated Savings
    """

    models = [
        "gemini-2.5-flash",
        "gemini-2.0-flash"
    ]

    for model in models:

        try:

            response = client.models.generate_content(
                model=model,
                contents=prompt
            )

            return response.text

        except Exception as e:

            error = str(e)

            if "429" in error or "RESOURCE_EXHAUSTED" in error:
                continue

            return f"AI report error: {error}"

    time.sleep(40)

    return "AI report unavailable due to API limits."