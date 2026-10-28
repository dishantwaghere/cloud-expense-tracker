# Cloud-Based Expense Tracker (Mini Project)

A beginner-friendly expense tracker with add/delete, total spending, transaction count, and category totals.

## Run on Windows
1. Extract the ZIP.
2. Open PowerShell in the `cloud_expense_tracker` folder.
3. Run these commands:

```powershell
py -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python app.py
```

4. Open http://127.0.0.1:5000 in a browser.

If PowerShell blocks activation, try:
```powershell
.venv\Scripts\python.exe -m pip install -r requirements.txt
.venv\Scripts\python.exe app.py
```

## Features
- Add an expense with description, amount, category and date.
- Show all saved expenses.
- Calculate total spending and transaction count.
- Show totals grouped by category.
- Delete an expense.
- Store records in a local SQLite database (`expenses.db`).

## Technologies
- Python + Flask: backend routes and request handling.
- HTML/CSS: dashboard UI.
- SQLite: local database.

## Honest cloud limitation
This ZIP runs locally; it is a prototype of a cloud-based application, not deployed cloud infrastructure. For actual cloud deployment, host the app and use a managed database such as Amazon RDS or a cloud database service. Add user login and authorization before storing real financial data. Do not enter real bank credentials or sensitive financial details.
