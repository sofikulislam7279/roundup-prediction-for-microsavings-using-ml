import gradio as gr

from roundup.pipeline.prediction_pipeline import RoundupPredictor


predictor = RoundupPredictor()


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


CSS = """
:root {
    --paper: #f5f8f5;
    --white: #ffffff;
    --ink: #10251c;
    --soft: #60736a;
    --forest: #027e65;
    --forest-dark: #07513e;
    --line: #e1e9e3;
}

/* Page */
body,
.gradio-container {
    background: var(--paper) !important;
    color: var(--ink) !important;
}

.gradio-container {
    max-width: 900px !important;
    margin: auto !important;
}

/* Header */
#header {
    padding: 20px 4px 12px;
}

#brand {
    font-size: 28px;
    font-weight: 700;
    color: var(--forest-dark);
    margin: 0;
}

#tagline {
    color: var(--soft);
    font-size: 14px;
    margin-top: 3px;
}

/* Form */
.form-area {
    background: var(--white);
    border: 1px solid var(--line);
    border-radius: 14px;
    padding: 18px;
}

/* Labels */
label span {
    color: var(--ink) !important;
}

/* Inputs */
input,
textarea,
select {
    border-color: var(--line) !important;
    border-radius: 8px !important;
}

/* Button */
#predict-btn {
    background: var(--forest) !important;
    color: white !important;
    border: none !important;
    border-radius: 8px !important;
    font-weight: 600;
    margin-top: 8px;
}

#predict-btn:hover {
    background: var(--forest-dark) !important;
}

/* Results */
.result-area {
    padding: 20px 4px 10px;
}

.result-title {
    color: var(--forest-dark);
    font-size: 17px;
    font-weight: 600;
    margin-bottom: 8px;
}

.result-box textarea {
    font-size: 22px !important;
    font-weight: 600 !important;
    color: var(--forest-dark) !important;
}

/* Footer */
#footer {
    text-align: center;
    color: var(--soft);
    font-size: 12px;
    padding: 18px 0;
}
"""


with gr.Blocks(
    title="Jomao — Adaptive Round-Up",
    css=CSS,
) as demo:

    # Header
    gr.HTML(
        """
        <div id="header">
            <div id="brand">Jomao</div>
            <div id="tagline">Adaptive round-up for smarter micro-savings</div>
        </div>
        """
    )

    with gr.Group(elem_classes="form-area"):

        # Transaction
        with gr.Row():
            txn_amount = gr.Number(
                label="Transaction Amount (৳)",
                value=285,
                minimum=0,
            )

            category = gr.Textbox(
                label="Category",
                value="Food",
            )

        # Spending
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

        # Savings profile
        with gr.Row():
            income_tier = gr.Dropdown(
                choices=["low", "middle", "high"],
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
            elem_id="predict-btn",
        )

    # Results
    with gr.Column(elem_classes="result-area"):

        gr.HTML(
            '<div class="result-title">Your adaptive round-up</div>'
        )

        with gr.Row():

            roundup_output = gr.Textbox(
                label="Round-up",
                value="—",
                interactive=False,
                elem_classes="result-box",
            )

            total_output = gr.Textbox(
                label="Total After Round-up",
                value="—",
                interactive=False,
                elem_classes="result-box",
            )

    gr.HTML(
        """
        <div id="footer">
            Jomao · ML-powered micro-savings
        </div>
        """
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
    demo.launch()