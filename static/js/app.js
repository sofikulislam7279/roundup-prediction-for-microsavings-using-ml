"use strict";

const form = document.getElementById("roundup-form");
const note = document.getElementById("form-note");
const receipt = document.getElementById("receipt");
const receiptEmpty = document.getElementById("receipt-empty");
const receiptBody = document.getElementById("receipt-body");
const submitBtn = document.getElementById("submit-btn");
const resetBtn = document.getElementById("reset-btn");

const numericFloatFields = [
  "txn_amount",
  "daily_total_spent",
  "avg_spend_last_7days",
  "monthly_savings_so_far",
];

const numericIntegerFields = [
  "txn_count_today",
  "txn_count_prev_7d",
  "user_tenure_days",
  "user_savings_streak",
  "days_since_last_txn",
];

const money = (value) => {
  const amount = Number(value);

  if (!Number.isFinite(amount)) {
    return "Tk 0.00";
  }

  return (
    "Tk " +
    amount.toLocaleString("en-BD", {
      minimumFractionDigits: 2,
      maximumFractionDigits: 2,
    })
  );
};

const getCurrentTime = () => {
  return new Date().toLocaleTimeString("en-BD", {
    hour: "2-digit",
    minute: "2-digit",
  });
};

const setNote = (message, isSuccess = false) => {
  note.textContent = message;
  note.classList.toggle("success", isSuccess);
};

const setLoading = (isLoading) => {
  submitBtn.disabled = isLoading;
  resetBtn.disabled = isLoading;

  submitBtn.querySelector(".btn-label").textContent = isLoading
    ? "Calculating..."
    : "Calculate round-up";

  submitBtn.querySelector(".btn-arrow").textContent = isLoading
    ? "…"
    : "↗";
};

const buildPayload = () => {
  const formData = new FormData(form);
  const payload = {};

  for (const [key, value] of formData.entries()) {
    if (numericFloatFields.includes(key)) {
      payload[key] = Number.parseFloat(value);
    } else if (numericIntegerFields.includes(key)) {
      payload[key] = Number.parseInt(value, 10);
    } else {
      payload[key] = value;
    }
  }

  return payload;
};

const validatePayload = (payload) => {
  for (const field of numericFloatFields) {
    if (
      typeof payload[field] !== "number" ||
      !Number.isFinite(payload[field]) ||
      payload[field] < 0
    ) {
      return `Please enter a valid value for ${field.replaceAll("_", " ")}.`;
    }
  }

  if (payload.txn_amount <= 0) {
    return "Transaction amount must be greater than zero.";
  }

  for (const field of numericIntegerFields) {
    if (
      typeof payload[field] !== "number" ||
      !Number.isInteger(payload[field]) ||
      payload[field] < 0
    ) {
      return `Please enter a valid whole number for ${field.replaceAll("_", " ")}.`;
    }
  }

  if (!payload.category) {
    return "Please choose a transaction category.";
  }

  if (!payload.income_tier) {
    return "Please choose an income tier.";
  }

  return null;
};

const showPrediction = (data) => {
  const originalAmount = Number(data.original_amount);
  const roundupAmount = Number(data.roundup_amount);
  const roundedTotal = Number(data.rounded_total);

  if (
    !Number.isFinite(originalAmount) ||
    !Number.isFinite(roundupAmount) ||
    !Number.isFinite(roundedTotal)
  ) {
    throw new Error("The server returned an invalid prediction.");
  }

  document.getElementById("r-original").textContent =
    money(originalAmount);

  document.getElementById("r-roundup-small").textContent =
    money(roundupAmount);

  document.getElementById("r-roundup").textContent =
    money(roundupAmount);

  document.getElementById("r-total").textContent =
    money(roundedTotal);

  document.getElementById("receipt-time").textContent =
    getCurrentTime();

  receiptEmpty.hidden = true;
  receiptBody.hidden = false;

  receipt.classList.remove("printing");

  // Restart the receipt animation.
  void receipt.offsetWidth;

  receipt.classList.add("printing");
};

form.addEventListener("submit", async (event) => {
  event.preventDefault();

  setNote("");

  if (!form.checkValidity()) {
    form.reportValidity();
    return;
  }

  let payload;

  try {
    payload = buildPayload();
  } catch {
    setNote("Please check the values in the form.");
    return;
  }

  const validationError = validatePayload(payload);

  if (validationError) {
    setNote(validationError);
    return;
  }

  setLoading(true);

  try {
    const response = await fetch("/predict", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Accept: "application/json",
      },
      body: JSON.stringify(payload),
    });

    let data;

    try {
      data = await response.json();
    } catch {
      throw new Error(
        "The server returned an invalid response."
      );
    }

    if (!response.ok) {
      throw new Error(
        data.error ||
          "Prediction failed. Please try again."
      );
    }

    showPrediction(data);

    setNote("Prediction generated successfully.", true);

  } catch (error) {
    console.error("Round-up prediction error:", error);

    setNote(
      error.message ||
        "Couldn't calculate this prediction. Check the numbers and try again."
    );

  } finally {
    setLoading(false);
  }
});

resetBtn.addEventListener("click", () => {
  form.reset();

  receiptEmpty.hidden = false;
  receiptBody.hidden = true;

  receipt.classList.remove("printing");

  setNote("");

  document.getElementById("r-original").textContent = "Tk 0.00";
  document.getElementById("r-roundup-small").textContent = "Tk 0.00";
  document.getElementById("r-roundup").textContent = "Tk 0.00";
  document.getElementById("r-total").textContent = "Tk 0.00";
  document.getElementById("receipt-time").textContent = "--:--";
});