"""
Personal Expense Tracker with CSV
---------------------------------
Record daily expenses by category and save them persistently to a CSV file.

Features:
  1. Add, view, and filter expenses
  2. CSV read/write operations using the csv module
  3. Category summary statistics
"""

import csv
import os
from datetime import datetime

FILE_NAME = "expenses.csv"
FIELDS = ["date", "category", "description", "amount"]
DATE_FORMAT = "%Y-%m-%d"


# ---------- CSV helpers ----------
def init_file():
    """Create the CSV file with a header row if it doesn't exist yet."""
    if not os.path.exists(FILE_NAME):
        with open(FILE_NAME, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=FIELDS)
            writer.writeheader()


def load_expenses():
    """Read all expenses from the CSV file and return them as a list of dicts."""
    expenses = []
    with open(FILE_NAME, "r", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                row["amount"] = float(row["amount"])
                expenses.append(row)
            except (ValueError, KeyError):
                continue  # skip corrupted rows
    return expenses


def save_expense(expense):
    """Append a single expense to the CSV file."""
    with open(FILE_NAME, "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDS)
        writer.writerow(expense)


# ---------- Input helpers ----------
def get_date(prompt, allow_blank=False):
    """Ask for a date (YYYY-MM-DD). Blank = today (or None if allow_blank)."""
    while True:
        value = input(prompt).strip()
        if not value:
            return None if allow_blank else datetime.now().strftime(DATE_FORMAT)
        try:
            return datetime.strptime(value, DATE_FORMAT).strftime(DATE_FORMAT)
        except ValueError:
            print("  Invalid date. Use YYYY-MM-DD (e.g. 2026-10-05).")


def get_amount():
    """Ask for a positive number."""
    while True:
        try:
            amount = float(input("Amount: ").strip())
            if amount <= 0:
                print("  Amount must be greater than 0.")
                continue
            return round(amount, 2)
        except ValueError:
            print("  Please enter a valid number.")


# ---------- Features ----------
def add_expense():
    print("\n--- Add Expense ---")
    date = get_date("Date (YYYY-MM-DD, press Enter for today): ")

    category = input("Category (e.g. Food, Transport, Bills): ").strip().title()
    while not category:
        category = input("Category cannot be empty. Try again: ").strip().title()

    description = input("Description: ").strip()
    amount = get_amount()

    save_expense(
        {"date": date, "category": category, "description": description, "amount": amount}
    )
    print("Expense saved!")


def print_table(expenses):
    """Pretty-print a list of expenses and their total."""
    if not expenses:
        print("  No expenses found.")
        return

    print(f"\n{'No.':<4} {'Date':<12} {'Category':<15} {'Description':<25} {'Amount':>10}")
    print("-" * 70)
    for i, e in enumerate(expenses, start=1):
        print(
            f"{i:<4} {e['date']:<12} {e['category']:<15} "
            f"{e['description'][:24]:<25} {e['amount']:>10.2f}"
        )
    print("-" * 70)
    total = sum(e["amount"] for e in expenses)
    print(f"{'TOTAL':<58} {total:>10.2f}")


def view_expenses():
    print("\n--- All Expenses ---")
    print_table(load_expenses())


def filter_expenses():
    print("\n--- Filter Expenses ---")
    print("1. By category")
    print("2. By date range")
    choice = input("Choose (1/2): ").strip()
    expenses = load_expenses()

    if choice == "1":
        category = input("Enter category: ").strip().lower()
        results = [e for e in expenses if e["category"].lower() == category]
    elif choice == "2":
        start = get_date("Start date (YYYY-MM-DD, Enter for no limit): ", allow_blank=True)
        end = get_date("End date   (YYYY-MM-DD, Enter for no limit): ", allow_blank=True)
        results = [
            e
            for e in expenses
            if (start is None or e["date"] >= start) and (end is None or e["date"] <= end)
        ]
    else:
        print("Invalid choice.")
        return

    print_table(results)


def category_summary():
    print("\n--- Category Summary ---")
    expenses = load_expenses()
    if not expenses:
        print("  No expenses recorded yet.")
        return

    summary = {}
    for e in expenses:
        summary.setdefault(e["category"], []).append(e["amount"])

    grand_total = sum(e["amount"] for e in expenses)

    print(
        f"\n{'Category':<15} {'Count':>5} {'Total':>10} {'Average':>10} "
        f"{'Min':>9} {'Max':>9} {'% of Total':>11}"
    )
    print("-" * 75)
    # Sort by highest total spending first
    for category, amounts in sorted(summary.items(), key=lambda x: sum(x[1]), reverse=True):
        total = sum(amounts)
        print(
            f"{category:<15} {len(amounts):>5} {total:>10.2f} {total / len(amounts):>10.2f} "
            f"{min(amounts):>9.2f} {max(amounts):>9.2f} {total / grand_total * 100:>10.1f}%"
        )
    print("-" * 75)
    print(f"{'GRAND TOTAL':<21} {grand_total:>10.2f}   ({len(expenses)} expenses)")


# ---------- Main menu ----------
def main():
    init_file()
    actions = {
        "1": add_expense,
        "2": view_expenses,
        "3": filter_expenses,
        "4": category_summary,
    }

    while True:
        print("\n===== Personal Expense Tracker =====")
        print("1. Add expense")
        print("2. View all expenses")
        print("3. Filter expenses")
        print("4. Category summary")
        print("5. Exit")
        choice = input("Choose an option (1-5): ").strip()

        if choice == "5":
            print("Goodbye!")
            break
        action = actions.get(choice)
        if action:
            action()
        else:
            print("Invalid choice. Please enter 1-5.")


if __name__ == "__main__":
    main()