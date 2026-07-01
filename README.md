# Lulu Sales Dashboard 🛒

An interactive Streamlit dashboard for exploring synthetic Lulu Hypermarket sales data —
built for stakeholder demos / classroom exercises.

## Features
- KPI summary: orders, units sold, net sales, profit, margin
- Sales trend over time (day / week / month)
- Sales breakdown by category, store, product, payment method, and channel
- Sidebar filters: date range, city, store, category, sales channel
- Filtered data table with CSV download

## Project structure
```
lulu_dashboard/
├── app.py                     # Streamlit app
├── data/
│   └── lulu_sales_data.csv    # Synthetic dataset (3,500 orders, FY2025)
├── requirements.txt
├── .streamlit/
│   └── config.toml            # Theme
└── .gitignore
```

## Run locally

```bash
# 1. Clone the repo
git clone https://github.com/<your-username>/lulu-sales-dashboard.git
cd lulu-sales-dashboard

# 2. Create a virtual environment (optional but recommended)
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the app
streamlit run app.py
```

The app will open at `http://localhost:8501`.

## Push to GitHub

```bash
cd lulu_dashboard
git init
git add .
git commit -m "Initial commit: Lulu sales dashboard"
git branch -M main
git remote add origin https://github.com/<your-username>/lulu-sales-dashboard.git
git push -u origin main
```

## Deploy for free on Streamlit Community Cloud
1. Push this folder to a public (or private) GitHub repo.
2. Go to [share.streamlit.io](https://share.streamlit.io) and sign in with GitHub.
3. Click **New app**, select your repo/branch, and set the main file path to `app.py`.
4. Click **Deploy** — you'll get a shareable public URL in a couple of minutes.

## Using your own data
Replace `data/lulu_sales_data.csv` with your own file, keeping the same column names,
or edit the `DATA_PATH` and column references in `app.py`. Expected columns:

`Order_ID, Order_Date, Store_ID, Store_Name, City, Category, Product, Unit_Cost_AED,
Unit_Price_AED, Quantity, Discount_Pct, Gross_Amount_AED, Discount_Amount_AED,
Net_Amount_AED, Cost_Amount_AED, Profit_AED, Payment_Method, Sales_Channel`

## Troubleshooting

**`FileNotFoundError` on Streamlit Cloud for `data/lulu_sales_data.csv`**
This almost always means the `data/` folder wasn't actually pushed to GitHub. Check:
1. On GitHub, open your repo in the browser and confirm `data/lulu_sales_data.csv` is there.
2. If it's missing, run `git status` locally — if the file is untracked, your `.gitignore`
   or upload method (e.g. drag-and-drop on github.com) may have skipped it. Run
   `git add data/lulu_sales_data.csv && git commit -m "Add data" && git push`.
3. Redeploy (or click "Reboot app" in Streamlit Cloud's "Manage app" panel).

`app.py` loads the CSV using a path relative to the script's own location, so it works
regardless of the app's working directory — no changes needed there.

## Notes
- The dataset is fully synthetic and generated for demo/teaching purposes — it does not
  reflect real Lulu Hypermarket sales figures.
