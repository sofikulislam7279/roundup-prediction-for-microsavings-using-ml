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

        roundup_amount = round(max(float(roundup_amount), 0.0), 2)
        rounded_total = round(
            float(txn_amount) + roundup_amount,
            2,
        )

        return (
            f"৳{roundup_amount:.2f}",
            f"৳{float(txn_amount):.2f}",
            f"৳{rounded_total:.2f}",
            "Prediction completed successfully.",
        )

    except Exception as e:
        return (
            "Error",
            "—",
            "—",
            f"Prediction failed: {str(e)}",
        )


# ==========================================================
# CSS
# ==========================================================

css = """
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Fraunces:opsz,wght@9..144,400;9..144,500;9..144,600&family=IBM+Plex+Mono:wght@400;500;600&display=swap');

:root {
    --paper: #f5f8f5;
    --white: #ffffff;
    --ink: #10251c;
    --soft: #60736a;
    --muted: #91a098;

    --forest: #027e65;
    --forest-dark: #07513e;
    --forest-light: #1ec677;
    --forest-pale: #e6f6ed;

    --line: #e1e9e3;
    --line-strong: #c8d5cc;
}


/* ==========================================================
   PAGE
   ========================================================== */

.gradio-container {
    max-width: 1080px !important;
    margin: auto !important;
    background: var(--paper) !important;
    font-family: "DM Sans", sans-serif !important;
    color: var(--ink) !important;
}

body {
    background: var(--paper) !important;
}


/* ==========================================================
   HEADER
   ========================================================== */

.jomao-header {
    height: 76px;

    display: flex;
    align-items: center;
    justify-content: space-between;

    border-bottom: 1px solid var(--line);
}

.brand {
    display: flex;
    align-items: center;
    gap: 10px;
}

.logo {
    width: 38px;
    height: 38px;

    display: grid;
    place-items: center;

    border-radius: 10px;

    background: var(--forest);
    color: white;

    font-family: "IBM Plex Mono", monospace;
    font-weight: 600;
}

.brand-name {
    color: var(--forest-dark);

    font-family: "Fraunces", Georgia, serif;
    font-size: 27px;
    font-weight: 600;

    letter-spacing: -1px;
}

.brand-name span {
    color: var(--forest-light);
}

.header-right {
    display: flex;
    align-items: center;
    gap: 8px;

    color: var(--soft);

    font-family: "IBM Plex Mono", monospace;
    font-size: 9px;
}

.dot {
    width: 7px;
    height: 7px;

    border-radius: 50%;

    background: var(--forest-light);
}


/* ==========================================================
   INTRO
   ========================================================== */

.intro {
    padding: 45px 0 35px;
}

.eyebrow {
    color: var(--forest);

    font-family: "IBM Plex Mono", monospace;
    font-size: 9px;
    font-weight: 600;

    letter-spacing: 1.2px;
}

.intro h1 {
    margin: 9px 0 10px;

    color: var(--forest-dark);

    font-family: "Fraunces", Georgia, serif;

    font-size: clamp(38px, 5vw, 52px);
    font-weight: 500;

    line-height: 1.1;
    letter-spacing: -2px;
}

.intro h1 em {
    color: var(--forest);
    font-style: italic;
}

.intro p {
    max-width: 550px;

    margin: 0;

    color: var(--soft);

    font-size: 13px;
    line-height: 1.7;
}


/* ==========================================================
   WORKSPACE
   ========================================================== */

.workspace {
    display: grid;

    grid-template-columns: 1.08fr .92fr;

    gap: 22px;

    align-items: start;
}


/* ==========================================================
   PANELS
   ========================================================== */

.panel {
    padding: 25px;

    background: var(--white);

    border: 1px solid var(--line);

    border-radius: 16px;
}


/* ==========================================================
   SECTION HEADERS
   ========================================================== */

.section-title {
    display: flex;
    align-items: center;

    gap: 9px;

    margin-bottom: 17px;

    color: var(--forest-dark);

    font-family: "Fraunces", Georgia, serif;

    font-size: 17px;
    font-weight: 500;
}

.number {
    width: 23px;
    height: 23px;

    display: grid;
    place-items: center;

    border-radius: 7px;

    background: var(--forest-pale);

    color: var(--forest);

    font-family: "IBM Plex Mono", monospace;

    font-size: 8px;
}

.section-description {
    margin: -8px 0 17px;

    color: var(--muted);

    font-size: 10px;
}


/* ==========================================================
   INPUTS
   ========================================================== */

.input-row {
    margin-bottom: 10px;
}

.panel label {
    color: var(--soft) !important;

    font-size: 10px !important;
    font-weight: 600 !important;
}

.panel input,
.panel textarea,
.panel select {
    border: 1px solid var(--line-strong) !important;

    border-radius: 8px !important;

    background: #fbfdfb !important;

    color: var(--ink) !important;

    font-size: 12px !important;
}

.panel input:focus {
    border-color: var(--forest) !important;

    box-shadow:
        0 0 0 3px rgba(2,126,101,.08) !important;
}


/* ==========================================================
   BUTTON
   ========================================================== */

.predict {
    margin-top: 13px !important;

    min-height: 48px !important;

    border: none !important;

    border-radius: 9px !important;

    background: var(--forest) !important;

    color: white !important;

    font-size: 12px !important;
    font-weight: 600 !important;
}

.predict:hover {
    background: var(--forest-dark) !important;
}

.reset {
    background: transparent !important;

    border: none !important;

    color: var(--soft) !important;

    font-size: 10px !important;
}


/* ==========================================================
   RESULT
   ========================================================== */

.result-panel {
    position: sticky;
    top: 20px;
}

.result-top {
    display: flex;
    justify-content: space-between;

    color: var(--muted);

    font-family: "IBM Plex Mono", monospace;

    font-size: 8px;

    letter-spacing: .8px;
}

.result-heading {
    margin-top: 25px;

    color: var(--forest);

    font-family: "IBM Plex Mono", monospace;

    font-size: 9px;

    letter-spacing: 1px;
}

.result-title {
    margin-top: 5px;

    color: var(--forest-dark);

    font-family: "Fraunces", Georgia, serif;

    font-size: 24px;
    font-weight: 500;
}


/* Main amount */

.amount {
    margin-top: 22px;

    padding: 24px 15px;

    text-align: center;

    background: var(--forest-pale);

    border: 1px solid #d2eddd;

    border-radius: 12px;
}

.amount-label {
    color: var(--muted);

    font-family: "IBM Plex Mono", monospace;

    font-size: 8px;

    letter-spacing: 1px;
}

.amount-value {
    margin: 7px 0 3px;

    color: var(--forest);

    font-family: "Fraunces", Georgia, serif;

    font-size: 43px;
    font-weight: 600;

    line-height: 1.1;

    letter-spacing: -1.5px;
}

.amount-caption {
    color: var(--soft);

    font-size: 10px;
}


/* Result details */

.result-details {
    margin-top: 12px;
}

.detail {
    padding: 13px;

    border-bottom: 1px solid var(--line);

    display: flex;
    justify-content: space-between;
    align-items: center;

    color: var(--soft);

    font-family: "IBM Plex Mono", monospace;

    font-size: 9px;
}

.detail strong {
    color: var(--ink);

    font-weight: 500;
}


/* Message */

.message {
    margin-top: 17px;

    text-align: center;

    color: var(--soft);

    font-family: "Fraunces", Georgia, serif;

    font-size: 12px;

    font-style: italic;
}


/* Disclaimer */

.disclaimer {
    margin-top: 18px;

    padding-top: 14px;

    border-top: 1px solid var(--line);

    color: var(--muted);

    font-size: 9px;

    line-height: 1.6;
}


/* ==========================================================
   FOOTER
   ========================================================== */

.footer {
    margin-top: 55px;

    padding: 22px 0 30px;

    border-top: 1px solid var(--line);

    display: flex;
    justify-content: space-between;

    color: var(--muted);

    font-size: 9px;
}

.footer strong {
    color: var(--forest-dark);

    font-family: "Fraunces", Georgia, serif;

    font-size: 17px;
}


/* ==========================================================
   MOBILE
   ========================================================== */

@media (max-width: 800px) {

    .workspace {
        grid-template-columns: 1fr;
    }

    .result-panel {
        position: static;
    }

}


@media (max-width: 600px) {

    .gradio-container {
        padding: 0 14px !important;
    }

    .header-right {
        display: none;
    }

    .intro {
        padding: 35px 0 28px;
    }

    .intro h1 {
        font-size: 38px;
    }

    .panel {
        padding: 19px;
    }

    .footer {
        flex-direction: column;
        gap: 8px;
    }
}
"""


# ==========================================================
# UI
# ==========================================================

with gr.Blocks(
    title="Jomao — Adaptive Round-Up Prediction",
    css=css,
    theme=gr.themes.Base(
        primary_hue="green",
        neutral_hue="slate",
        font=[
            gr.themes.GoogleFont("DM Sans"),
            "sans-serif",
        ],
    ),
) as demo:

    # ------------------------------------------------------
    # Header
    # ------------------------------------------------------

    gr.HTML(
        """
        <header class="jomao-header">

            <div class="brand">

                <div class="logo">৳</div>

                <div class="brand-name">
                    Jom<span>ao</span>
                </div>

            </div>

            <div class="header-right">

                <span class="dot"></span>

                <span>ADAPTIVE ROUND-UP ENGINE</span>

            </div>

        </header>
        """
    )


    # ------------------------------------------------------
    # Intro
    # ------------------------------------------------------

    gr.HTML(
        """
        <section class="intro">

            <div class="eyebrow">
                MICRO-SAVINGS · MACHINE LEARNING
            </div>

            <h1>
                Turn every payment into
                <em>a little savings.</em>
            </h1>

            <p>
                Jomao predicts a personalised round-up amount
                using transaction behaviour and savings patterns.
            </p>

        </section>
        """
    )


    # ------------------------------------------------------
    # Workspace
    # ------------------------------------------------------

    with gr.Row(elem_classes="workspace"):

        # ==================================================
        # INPUT PANEL
        # ==================================================

        with gr.Column(elem_classes="panel"):

            # ------------------------------------------------
            # Transaction
            # ------------------------------------------------

            gr.HTML(
                """
                <div class="section-title">
                    <span class="number">01</span>
                    Transaction
                </div>

                <div class="section-description">
                    Information about the current payment.
                </div>
                """
            )

            with gr.Row(elem_classes="input-row"):

                txn_amount = gr.Number(
                    label="Transaction Amount (৳)",
                    value=285,
                    minimum=0,
                )

                category = gr.Dropdown(
                    choices=[
                        "Food",
                        "Transport",
                        "Shopping",
                        "Bills",
                        "Entertainment",
                        "Healthcare",
                        "Education",
                        "Groceries",
                        "Other",
                    ],
                    value="Food",
                    label="Merchant Category",
                )


            # ------------------------------------------------
            # Behaviour
            # ------------------------------------------------

            gr.HTML(
                """
                <div class="section-title">
                    <span class="number">02</span>
                    Spending Behaviour
                </div>

                <div class="section-description">
                    Recent activity and spending signals.
                </div>
                """
            )

            with gr.Row(elem_classes="input-row"):

                txn_count_today = gr.Number(
                    label="Transactions Today",
                    value=3,
                    minimum=0,
                    precision=0,
                )

                daily_total_spent = gr.Number(
                    label="Daily Total Spent (৳)",
                    value=1250,
                    minimum=0,
                )


            with gr.Row(elem_classes="input-row"):

                txn_count_prev_7d = gr.Number(
                    label="Transactions — Previous 7 Days",
                    value=18,
                    minimum=0,
                    precision=0,
                )

                avg_spend_last_7days = gr.Number(
                    label="Average Spend — Last 7 Days (৳)",
                    value=420,
                    minimum=0,
                )


            # ------------------------------------------------
            # Profile
            # ------------------------------------------------

            gr.HTML(
                """
                <div class="section-title">
                    <span class="number">03</span>
                    Profile & Savings
                </div>

                <div class="section-description">
                    User context and savings behaviour.
                </div>
                """
            )

            with gr.Row(elem_classes="input-row"):

                income_tier = gr.Dropdown(
                    choices=[
                        "low",
                        "middle",
                        "high",
                    ],
                    value="middle",
                    label="Income Tier",
                )

                user_tenure_days = gr.Number(
                    label="User Tenure (Days)",
                    value=180,
                    minimum=0,
                    precision=0,
                )


            with gr.Row(elem_classes="input-row"):

                monthly_savings_so_far = gr.Number(
                    label="Monthly Savings (৳)",
                    value=850,
                    minimum=0,
                )

                user_savings_streak = gr.Number(
                    label="Savings Streak",
                    value=12,
                    minimum=0,
                    precision=0,
                )


            days_since_last_txn = gr.Number(
                label="Days Since Last Transaction",
                value=1,
                minimum=0,
                precision=0,
            )


            # ------------------------------------------------
            # Buttons
            # ------------------------------------------------

            predict_btn = gr.Button(
                "Predict Adaptive Round-Up",
                elem_classes="predict",
                variant="primary",
            )

            reset_btn = gr.Button(
                "Reset example",
                elem_classes="reset",
            )


        # ==================================================
        # RESULT PANEL
        # ==================================================

        with gr.Column(elem_classes="panel result-panel"):

            gr.HTML(
                """
                <div class="result-top">

                    <span>JOMAO / RECEIPT</span>

                    <span>ML ENGINE</span>

                </div>

                <div class="result-heading">
                    PREDICTION RESULT
                </div>

                <div class="result-title">
                    Your micro-saving
                </div>
                """
            )


            roundup_output = gr.Textbox(
                value="—",
                label="Predicted Round-Up",
                interactive=False,
                elem_classes="amount",
            )


            gr.HTML(
                """
                <div class="amount-caption">
                    Suggested amount to add to your savings wallet.
                </div>
                """
            )


            gr.HTML(
                """
                <div class="result-details">

                    <div class="detail">
                        <span>TRANSACTION</span>
                        <strong id="original">—</strong>
                    </div>

                    <div class="detail">
                        <span>AFTER ROUND-UP</span>
                        <strong id="total">—</strong>
                    </div>

                </div>
                """
            )


            original_output = gr.Textbox(
                value="—",
                label="Transaction",
                interactive=False,
                visible=False,
            )

            total_output = gr.Textbox(
                value="—",
                label="After Round-Up",
                interactive=False,
                visible=False,
            )


            message_output = gr.Textbox(
                value="Ready for prediction.",
                label="",
                interactive=False,
                elem_classes="message",
            )


            gr.HTML(
                """
                <div class="disclaimer">
                    ⓘ Model-generated prediction for demonstration
                    purposes. This is not financial advice.
                </div>
                """
            )


    # ======================================================
    # Footer
    # ======================================================

    gr.HTML(
        """
        <footer class="footer">

            <strong>Jomao</strong>

            <span>
                Adaptive Round-Up Prediction · ML Prototype
            </span>

        </footer>
        """
    )


    # ======================================================
    # Prediction
    # ======================================================

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
            original_output,
            total_output,
            message_output,
        ],
    )


    # ======================================================
    # Reset
    # ======================================================

    reset_btn.click(
        fn=lambda: (
            285,
            "Food",
            3,
            1250,
            18,
            420,
            "middle",
            180,
            850,
            12,
            1,
            "—",
            "—",
            "—",
            "Ready for prediction.",
        ),

        inputs=[],

        outputs=[
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
            roundup_output,
            original_output,
            total_output,
            message_output,
        ],
    )


# ==========================================================
# Launch
# ==========================================================

if __name__ == "__main__":
    demo.launch()

