from flask import Flask, request, redirect, url_for, render_template, flash
import sqlite3
from pathlib import Path

app=Flask(__name__); app.secret_key="dev-only-change-me"
DB=Path(__file__).parent/"instance"/"inventory.sqlite3"
DB.parent.mkdir(exist_ok=True)
def connect():
    c=sqlite3.connect(DB); c.row_factory=sqlite3.Row; return c
def init_db():
    with connect() as c: c.execute("CREATE TABLE IF NOT EXISTS items(id INTEGER PRIMARY KEY, sku TEXT UNIQUE NOT NULL, name TEXT NOT NULL, category TEXT NOT NULL DEFAULT '', quantity INTEGER NOT NULL DEFAULT 0, reorder_level INTEGER NOT NULL DEFAULT 5)")
init_db()
@app.get("/")
def index():
    q=request.args.get("q","").strip()
    with connect() as c: rows=c.execute("SELECT * FROM items WHERE name LIKE ? OR sku LIKE ? ORDER BY name",(f"%{q}%",f"%{q}%")).fetchall()
    return render_template("index.html",items=rows,q=q)
@app.post("/items")
def add_item():
    sku=request.form.get("sku","").strip(); name=request.form.get("name","").strip(); category=request.form.get("category","").strip(); quantity=request.form.get("quantity",0,type=int); reorder=request.form.get("reorder_level",5,type=int)
    if not sku or not name or quantity<0 or reorder<0: flash("Enter a SKU and item name; stock values cannot be negative.","error"); return redirect(url_for("index"))
    try:
        with connect() as c: c.execute("INSERT INTO items(sku,name,category,quantity,reorder_level) VALUES(?,?,?,?,?)",(sku,name,category,quantity,reorder))
        flash("Item added.","success")
    except sqlite3.IntegrityError: flash("That SKU is already in use.","error")
    return redirect(url_for("index"))
@app.post("/items/<int:item_id>/adjust")
def adjust(item_id):
    delta=request.form.get("delta",0,type=int)
    with connect() as c:
        row=c.execute("SELECT quantity FROM items WHERE id=?",(item_id,)).fetchone()
        if row and row["quantity"]+delta>=0: c.execute("UPDATE items SET quantity=quantity+? WHERE id=?",(delta,item_id)); flash("Stock updated.","success")
        else: flash("Item missing or adjustment would make stock negative.","error")
    return redirect(url_for("index"))
@app.post("/items/<int:item_id>/delete")
def delete(item_id):
    with connect() as c: c.execute("DELETE FROM items WHERE id=?",(item_id,))
    flash("Item removed.","success"); return redirect(url_for("index"))
if __name__=="__main__": app.run(debug=True)
