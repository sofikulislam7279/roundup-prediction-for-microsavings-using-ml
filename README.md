# Jomao — Adaptive Round-Up Prediction for Micro-Savings

> **ML Framework for Behavior-Aware Round-Up Prediction** | bKash · Nagad · Rocket

---

## 🚀 Live Demo

### Try Jomao Online

**[▶️ Open Jomao — Hugging Face Demo](https://huggingface.co/spaces/sofikulislam/jomao-roundup-prediction)**

Jomao is available as an interactive Gradio application on Hugging Face Spaces.

Open the application, enter the transaction and user information, and click **Predict Round-up**.

---

## 📌 Research Context

Bangladesh's Mobile Financial Services (MFS) ecosystem processes hundreds of millions of transactions annually, yet no intelligent mechanism exists for converting everyday payments into automatic savings. Jomao builds a supervised regression model that predicts a personalized, behavior-aware round-up amount for each **Make Payment** transaction in real time.

```text
Round-Up Amount (Tk) =
f(Transaction Amount,
  User Behavior,
  Financial State,
  Historical Patterns)
```

## ❓ Problem Statement

Fixed round-up systems ignore user-specific behavioral and financial patterns. There is no data-driven framework to answer:

> Given a user's transaction amount, historical behavior, and financial state — what is the optimal round-up amount for this payment?

## 💡 Solution

A machine-learning regression model that learns the interaction between transaction amount, income tier, intraday pressure signals, and historical spending patterns to predict an adaptive round-up that is both meaningful and fair.

## 🔬 Research Significance

This project enables:

- Personalized micro-savings prediction
- Behavior-aware financial modeling
- Real-time adaptive rounding systems

It demonstrates that round-up amounts can be learned from user behavior rather than fixed rules, making micro-savings more efficient and user-friendly.

Potential applications include:

- Personalized micro-savings
- Behavioral financial modeling
- Digital wallet savings
- Automated savings assistance
- Adaptive financial technology systems

### Research Direction

> **ML Framework for Adaptive, Behavior-Aware Round-Up Predictions from User Spending Sequences**

The objective is to investigate how machine learning can transform fixed round-up mechanisms into personalized micro-savings recommendations.

---

## 🧠 How It Works

```text
Digital Transaction
        │
        ▼
Transaction & User Features
        │
        ▼
Feature Processing
        │
        ▼
ML Regression Model
        │
        ▼
Adaptive Round-Up Amount
        │
        ▼
Micro-Savings Wallet
```

The model uses transaction and user-level behavioral features to estimate a suitable round-up amount. The predicted amount can then be added to a dedicated savings wallet.

---

## 🎯 Example

Suppose a user makes a digital payment:

```text
Transaction Amount = Tk 285
```

Instead of always applying a fixed rounding rule, Jomao predicts:

```text
Predicted Round-Up = Tk 11.50
```

The resulting amount becomes:

```text
Original Transaction = Tk 285.00
Adaptive Savings     = Tk  15.00
--------------------------------
Total                = Tk 300.00
```

The predicted amount depends on the learned behavior of the user and the transaction context.

> This is an illustrative example, not a measured model prediction.

---

## 📊 Dataset

The project uses a synthetically generated structured transactional dataset designed for machine-learning-based micro-savings prediction. The dataset represents digital-payment patterns and contains transaction-level behavioral and financial features.

### Schema

```text
Identifiers / metadata
├── txn_id
├── user_id
└── timestamp

Input features
├── txn_amount
├── category
├── transaction_hour
├── is_weekend
├── hour_sin
├── hour_cos
├── txn_count_today
├── daily_total_spent
├── remaining_daily_capacity
├── txn_count_prev_7d
├── avg_spend_last_7days
├── spending_velocity_ratio
├── income_tier
├── user_tenure_days
├── is_new_user
├── pressure_score
├── monthly_savings_so_far
├── user_savings_streak
├── days_since_last_txn
├── clean_number_tier
└── rounded_amount

Target
└── roundup_amount
```

### Target Variable

```text
roundup_amount
```

The target represents the adaptive round-up amount in Bangladeshi Taka (BDT).

---

## 🤖 Machine Learning

This project is formulated as a supervised regression problem.

### Candidate Models

- Linear Regression
- Ridge Regression
- Lasso Regression
- Support Vector Regression (SVR)
- K-Nearest Neighbors Regression
- Random Forest Regression
- Histogram Gradient Boosting
- AdaBoost
- XGBoost
- CatBoost

### Evaluation Metrics

| Metric | Purpose |
|---|---|
| RMSE | Measures prediction error with greater penalty for larger errors |
| MAE | Measures average absolute prediction error |
| R² Score | Measures explained variance relative to a baseline |

### Important Research Note

The current dataset is synthetic. Model performance on synthetic data does not establish real-world predictive accuracy. Real transaction data and user acceptance feedback would be required for meaningful real-world validation.

---

## 🏗️ Project Architecture

The project follows a modular, production-style machine learning pipeline.

```text
Data Ingestion
      │
      ▼
Data Validation
      │
      ▼
Data Transformation
      │
      ▼
Model Training
      │
      ▼
Model Evaluation
      │
      ▼
Model Pusher
      │
      ▼
Hugging Face Model Storage
      │
      ▼
Prediction Pipeline
      │
      ▼
FastAPI Application
```

---

## 📁 Project Structure

```text
roundup-prediction-for-microsavings-using-ml/
│
├── .github/
│   └── workflows/
│       └── ci-cd.yml
│
├── config/
│   ├── schema.yaml
│   └── model.yaml
│
├── notebooks/
│
├── roundup/
│   ├── cloud_storage/
│   │   └── storage_service.py
│   │
│   ├── components/
│   │   ├── data_ingestion.py
│   │   ├── data_validation.py
│   │   ├── data_transformation.py
│   │   ├── model_trainer.py
│   │   ├── model_evaluation.py
│   │   └── model_pusher.py
│   │
│   ├── configuration/
│   │   ├── hf_connection.py
│   │   └── mongodb_connection.py
│   │
│   ├── constants/
│   │
│   ├── data_access/
│   │   └── data.py
│   │
│   ├── entity/
│   │   ├── artifact_entity.py
│   │   ├── config_entity.py
│   │   ├── estimator.py
│   │   └── hf_estimator.py
│   │
│   ├── exception/
│   │
│   ├── logger/
│   │
│   ├── pipeline/
│   │   ├── training_pipeline.py
│   │   └── prediction_pipeline.py
│   │
│   ├── utils/
│   │   ├── common_utils.py
│   │   └── model_utils.py
│   
│
├── static/
│
├── templates/
│
├── .env.example
├── .gitignore
├── app.py
├── Dockerfile
├── gradio_app.py
├── requirements.txt
├── template.py
├── pyproject.toml
├── test.py
├── Dockerfile
├── .dockerignore
└── README.md

```

---

## 🚀 API

The project provides a FastAPI application for real-time round-up prediction.

### Health Check

```http
GET /health
```

Example response:

```json
{
  "status": "healthy",
  "model_loaded": true
}
```

### Prediction

```http
POST /predict
```

Example request:

```json
{
  "txn_amount": 285,
  "category": "Food",
  "txn_count_today": 3,
  "daily_total_spent": 1250,
  "txn_count_prev_7d": 18,
  "avg_spend_last_7days": 420,
  "income_tier": "middle",
  "user_tenure_days": 180,
  "monthly_savings_so_far": 850,
  "user_savings_streak": 12,
  "days_since_last_txn": 1
}
```

Example response:

```json
{
  "original_amount": 285.0,
  "roundup_amount": 15.0,
  "rounded_total": 300.0
}
```

---

## 💻 Running Locally

### 1. Clone the Repository

```bash
git clone https://github.com/sofikulislam7279/roundup-prediction-for-microsavings-using-ml.git

cd roundup-prediction-for-microsavings-using-ml
```

### 2. Create the Conda Environment

Python 3.10 is used for this project.

```bash
conda create -n roundup_env python=3.10

conda activate roundup_env
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the FastAPI Application

```bash
uvicorn app:app --host 0.0.0.0 --port 8000
```

### 5. Open the Application

```text
http://localhost:8000
```

### FastAPI Documentation

```text
http://localhost:8000/docs
```

---

## 🔐 Environment Variables

Create a `.env` file for local development.

```env
HF_TOKEN=your_huggingface_token

MONGODB_URL=your_mongodb_connection_string

APP_HOST=0.0.0.0
APP_PORT=8000
```

> Never commit `.env` files or secret tokens to GitHub.

---

## 🤗 Model Storage

The production model is stored in Hugging Face.

### Model Repository

```text
sofikulislam/roundup-model-bucket
```

### Model Path

```text
models/model.pkl
```

The prediction pipeline loads the production model from Hugging Face. The Hugging Face access token is provided through:

```text
HF_TOKEN
```

---

## 🔄 CI/CD Architecture

The project is designed around a GitHub-based CI/CD workflow.

```text
Developer
    │
    ▼
GitHub Repository
    │
    ▼
GitHub Actions
    │
    ├── Install dependencies
    ├── Python syntax check
    ├── Application import test
    └── Docker image build
    │
    ▼
Hugging Face Gradio Space
    │
    ▼
FastAPI Application
    │
    ▼
Jomao Prediction API
```

### CI Pipeline

GitHub Actions is used to automatically validate the application when changes are pushed to the `main` branch.

The CI pipeline performs:

1. Repository checkout.
2. Python 3.10 setup.
3. Dependency installation.
4. Python syntax validation.
5. FastAPI application import test.
6. Docker image build.

After successful CI validation, the deployment stage can synchronize the application with the Hugging Face Docker Space.

---

## 🛠️ Technology Stack

### Machine Learning

- Python
- Pandas
- NumPy
- Scikit-learn
- XGBoost
- CatBoost

### Backend

- FastAPI
- Uvicorn
- Pydantic

### Data & Storage

- MongoDB
- Hugging Face Hub

### Deployment

- Docker
- GitHub Actions
- Hugging Face Spaces & Buckets

### Development

- Git
- GitHub
- Conda
- Python 3.10

---

## ⚠️ Limitations

- The current dataset is synthetically generated for research and development purposes.
- The model has not been validated on appropriate real transaction data.
- Synthetic-data performance should not be interpreted as evidence of real-world financial behavior.
- Real user acceptance and savings outcomes require further study.
- The current system is a research prototype and does not constitute financial advice.

---

## 🔮 Future Work

Potential future extensions include:

- Real-world transaction data validation.
- Personalized savings-goal optimization.
- Online and incremental learning.
- User-level reinforcement learning.
- Explainable round-up recommendations.
- Real-time transaction integration.
- bKash/Nagad/Rocket API integration where officially available.
- Savings-goal-aware prediction.
- A/B testing of adaptive versus fixed round-up strategies.

---

## 📌 Project Status

**Status:** Research Prototype / Active Development

The project is focused on developing a machine-learning framework for adaptive round-up prediction and exploring its potential use in personalized micro-savings.

---

## 👨‍💻 Author

**Sofikul Islam**

Computer Science & Engineering Student
Islamic University, Bangladesh

GitHub: [@sofikulislam7279](https://github.com/sofikulislam7279)

---

## 📄 License

This project is intended for research, educational, and prototype development purposes.
