import pandas as pd

def analyze_ads(file_path):

    df = pd.read_csv(file_path)

    if df["CTR"].dtype == object:
        df["CTR"] = df["CTR"].astype(str).str.replace("%","").astype(float)

    issues = []
    campaign_waste = []
    wasted_spend = 0

    avg_cpc = df["CPC"].mean()

    for _, row in df.iterrows():

        waste = 0

        if row["Spend"] > 5000 and row["Conversions"] == 0:
            issues.append(
                f"{row['Campaign']} spent ₹{row['Spend']} with zero conversions."
            )
            waste += row["Spend"]

        if row["CPC"] > avg_cpc * 1.3:
            issues.append(
                f"{row['Campaign']} CPC significantly above account average."
            )
            waste += row["Spend"] * 0.3

        if row["CTR"] < 1:
            issues.append(
                f"{row['Campaign']} has low CTR indicating weak ad creative."
            )
            waste += row["Spend"] * 0.2

        if waste > 0:
            campaign_waste.append({
                "campaign": row["Campaign"],
                "waste": round(waste,2)
            })

        wasted_spend += waste

    total_spend = df["Spend"].sum()

    waste_percent = round((wasted_spend / total_spend) * 100, 2)

    waste_score = max(0, min(100, round(100 - (waste_percent * 2), 2)))

    if waste_score >= 80:
        status = "Good"
    elif waste_score >= 60:
        status = "Needs Optimization"
    else:
        status = "Critical Waste"

    campaign_waste = sorted(
        campaign_waste,
        key=lambda x: x["waste"],
        reverse=True
    )

    return {
        "total_spend": float(total_spend),
        "wasted_spend": float(round(wasted_spend,2)),
        "waste_percent": waste_percent,
        "waste_score": waste_score,
        "status": status,
        "campaign_waste": campaign_waste[:3],
        "issues": issues
    }