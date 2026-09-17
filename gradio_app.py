import gradio as gr
import spaces

from roundup.pipeline.prediction_pipeline import RoundupPredictor


# Load model once when the Space starts
predictor = RoundupPredictor()


@spaces.GPU
def predict_roundup(
    txn_amount,
    category,
    txn_count_today,
    daily_total_spent,
    txn_count_prev_7d,
    avg_spend_last_7days,
    income_tier,
    user_tenure_days,
    monthly_savings_so_far,
    user_savings_streak,
    days_since_last_txn,
):
    try:
        roundup_amount = predictor.predict(
            txn_amount=float(txn_amount),
            category=category,
            txn_count_today=int(txn_count_today),
            daily_total_spent=float(daily_total_spent),
            txn_count_prev_7d=int(txn_count_prev_7d),
            avg_spend_last_7days=float(avg_spend_last_7days),
            income_tier=income_tier,
            user_tenure_days=int(user_tenure_days),
            monthly_savings_so_far=float(monthly_savings_so_far),
            user_savings_streak=int(user_savings_streak),
            days_since_last_txn=int(days_since_last_txn),
        )

        roundup_amount = round(max(float(roundup_amount), 0.0), 2)
        rounded_total = round(float(txn_amount) + roundup_amount, 2)

        return (
            f"৳{roundup_amount:.2f}",
            f"৳{rounded_total:.2f}",
        )

    except Exception as e:
        return (
            f"Error: {str(e)}",
            "Unable to calculate",
        )


demo = gr.Interface(
    fn=predict_roundup,
    inputs=[
        gr.Number(
            label="Transaction Amount (৳)",
            value=285,
            minimum=0,
        ),
        gr.Textbox(
            label="Category",
            value="Food",
        ),
        gr.Number(
            label="Transactions Today",
            value=3,
            precision=0,
            minimum=0,
        ),
        gr.Number(
            label="Daily Total Spent (৳)",
            value=1250,
            minimum=0,
        ),
        gr.Number(
            label="Transactions in Previous 7 Days",
            value=18,
            precision=0,
            minimum=0,
        ),
        gr.Number(
            label="Average Spend Last 7 Days (৳)",
            value=420,
            minimum=0,
        ),
        gr.Dropdown(
            choices=["low", "middle", "high"],
            label="Income Tier",
            value="middle",
        ),
        gr.Number(
            label="User Tenure (Days)",
            value=180,
            precision=0,
            minimum=0,
        ),
        gr.Number(
            label="Monthly Savings So Far (৳)",
            value=850,
            minimum=0,
        ),
        gr.Number(
            label="Savings Streak",
            value=12,
            precision=0,
            minimum=0,
        ),
        gr.Number(
            label="Days Since Last Transaction",
            value=1,
            precision=0,
            minimum=0,
        ),
    ],
    outputs=[
        gr.Textbox(label="Predicted Round-up"),
        gr.Textbox(label="Total After Round-up"),
    ],
    title="Jomao — Adaptive Round-Up Prediction",
    description=(
        "Enter your transaction and spending information "
        "to predict an adaptive micro-savings round-up."
    ),
)


if __name__ == "__main__":
    demo.launch()