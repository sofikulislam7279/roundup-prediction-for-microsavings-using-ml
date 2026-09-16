const form = document.getElementById("roundup-form");
const note = document.getElementById("form-note");
const receipt = document.getElementById("receipt");
const receiptEmpty = document.getElementById("receipt-empty");
const receiptBody = document.getElementById("receipt-body");
const submitBtn = form.querySelector(".submit-btn");

const money = (value) =>
  "Tk " +
  Number(value).toLocaleString("en-BD", {
    minimumFractionDigits: 2,
    maximumFractionDigits: 2,
  });

form.addEventListener("submit", async (event) => {
  event.preventDefault();
  note.textContent = "";

  const formData = new FormData(form);
  const payload = {};
  for (const [key, value] of formData.entries()) {
    if (["txn_amount", "daily_total_spent", "avg_spend_last_7days", "monthly_savings_so_far"].includes(key)) {
      payload[key] = parseFloat(value);
    } else if (["category", "income_tier"].includes(key)) {
      payload[key] = value;
    } else {
      payload[key] = parseInt(value, 10);
    }
  }

  submitBtn.disabled = true;
  submitBtn.querySelector(".btn-label").textContent = "Calculating...";

  try {
    const response = await fetch("/predict", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });

    const data = await response.json();

    if (!response.ok) {
      throw new Error(data.error || "Something went wrong.");
    }

    document.getElementById("r-original").textContent = money(data.original_amount);
    document.getElementById("r-total").textContent = money(data.rounded_total);
    document.getElementById("r-roundup").textContent = money(data.roundup_amount);

    receiptEmpty.hidden = true;
    receiptBody.hidden = false;
    receipt.classList.remove("printing");
    void receipt.offsetWidth; // restart animation
    receipt.classList.add("printing");
  } catch (err) {
    note.textContent = err.message || "Couldn't calculate this one. Check the numbers and try again.";
  } finally {
    submitBtn.disabled = false;
    submitBtn.querySelector(".btn-label").textContent = "Calculate round-up";
  }
});