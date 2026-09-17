import gradio as gr
import spaces

from roundup.pipeline.prediction_pipeline import RoundupPredictor

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

        roundup_amount = round(
            max(float(roundup_amount), 0.0),
            2,
        )

        rounded_total = round(
            float(txn_amount) + roundup_amount,
            2,
        )

        return (
            f"৳{roundup_amount:.2f}",
            f"৳{rounded_total:.2f}",
        )

    except Exception as e:
        return (
            f"Error: {str(e)}",
            "Unable to calculate",
        )


theme = gr.themes.Soft(
    primary_hue="green",
    secondary_hue="emerald",
    neutral_hue="slate",
)



with gr.Blocks() as demo:

    gr.Markdown(
        """
        ### Adaptive Round-Up Prediction

        Predict an adaptive micro-savings amount from your
        transaction and spending behavior.
        """
    )


    gr.Markdown("### Transaction")

    with gr.Row():

        txn_amount = gr.Number(
            label="Transaction Amount (৳)",
            value=285,
            minimum=0,
        )

        category = gr.Dropdown(
            choices=[
                "food_delivery",
                "ride_sharing",
                "shopping",
                "ecommerce",
            ],
            label="Category",
            value="food_delivery",
        )

    gr.Markdown("### Spending Behavior")

    with gr.Row():

        txn_count_today = gr.Number(
            label="Transactions Today",
            value=3,
            precision=0,
            minimum=0,
        )

        daily_total_spent = gr.Number(
            label="Daily Total Spent (৳)",
            value=1250,
            minimum=0,
        )

    with gr.Row():

        txn_count_prev_7d = gr.Number(
            label="Transactions Previous 7 Days",
            value=18,
            precision=0,
            minimum=0,
        )

        avg_spend_last_7days = gr.Number(
            label="Average Spend Last 7 Days (৳)",
            value=420,
            minimum=0,
        )

    gr.Markdown("### Savings Profile")

    with gr.Row():

        income_tier = gr.Dropdown(
            choices=[
                "low",
                "middle",
                "high",
            ],
            label="Income Tier",
            value="middle",
        )

        user_tenure_days = gr.Number(
            label="User Tenure (Days)",
            value=180,
            precision=0,
            minimum=0,
        )

    with gr.Row():

        monthly_savings_so_far = gr.Number(
            label="Monthly Savings So Far (৳)",
            value=850,
            minimum=0,
        )

        user_savings_streak = gr.Number(
            label="Savings Streak",
            value=12,
            precision=0,
            minimum=0,
        )

    days_since_last_txn = gr.Number(
        label="Days Since Last Transaction",
        value=1,
        precision=0,
        minimum=0,
    )


    predict_btn = gr.Button(
        "Predict Round-up",
        variant="primary",
    )

    gr.Markdown("### Prediction")

    with gr.Row():

        roundup_output = gr.Textbox(
            label="Predicted Round-up",
            interactive=False,
        )

        total_output = gr.Textbox(
            label="Total After Round-up",
            interactive=False,
        )


    predict_btn.click(
        fn=predict_roundup,
        inputs=[
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
        ],
        outputs=[
            roundup_output,
            total_output,
        ],
    )



if __name__ == "__main__":
    demo.launch(
        theme=theme,
    )