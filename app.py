from flask import Flask, render_template, request, redirect, url_for
import time

app = Flask(__name__)

# Data structures
expenses = {}        # category -> total amount
transactions = []    # list of (category, amount, timestamp)
undo_stack = []      # stack for undo feature


def add_expense(category, amount):
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    transactions.append((category, amount, timestamp))  # store transaction
    undo_stack.append((category, amount))  # push to undo stack

    if category in expenses:
        expenses[category] += amount
    else:
        expenses[category] = amount


def undo_last_expense():
    if undo_stack:
        category, amount = undo_stack.pop()
        expenses[category] -= amount
        if expenses[category] == 0:
            del expenses[category]  # remove empty category
        transactions.pop()


@app.route("/")
def home():
    total = sum(expenses.values())
    sorted_expenses = sorted(expenses.items(), key=lambda x: x[1], reverse=True)
    return render_template("index.html",
                           expenses=expenses,
                           total=total,
                           transactions=transactions,
                           sorted_expenses=sorted_expenses)


@app.route("/add", methods=["POST"])
def add():
    category = request.form["category"]
    amount = int(request.form["amount"])
    add_expense(category, amount)
    return redirect(url_for("home"))


@app.route("/undo")
def undo():
    undo_last_expense()
    return redirect(url_for("home"))


if __name__ == "__main__":
    app.run(debug=True)
