# Stockroom Inventory

A Flask + SQLite inventory manager with SKU uniqueness, search, low-stock flags, stock adjustments, and item removal. It runs locally and stores records in an ignored SQLite database under `instance/`.

## Run

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python app.py
```

Open http://127.0.0.1:5000. For an internet-facing deployment, replace the development secret, disable debug mode, and add authentication and CSRF protection.

### Category

Web development | Python, Flask, SQLite, HTML/CSS
