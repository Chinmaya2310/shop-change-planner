"""Suggest which coins and notes a shop should keep ready as change."""
import csv
import sys
from collections import Counter
from datetime import datetime

NOTES = [50, 100, 500]            # what a customer might hand over
CHANGE = [200, 100, 50, 20, 10, 5, 2, 1]
MIN_ROWS = 20
PLAN_FOR = 10                     # suggest change for this many bills
COLUMNS = ["id", "date", "time", "amount", "notes"]

def check(row, seen):
    """Return the reason a row is bad, or None."""
    if None in row or any(row[c] is None for c in COLUMNS):
        return "wrong number of columns"
    if not row["id"].strip():
        return "blank id"
    if row["id"].strip() in seen:
        return "duplicate id"
    try:
        when = datetime.strptime(row["date"] + " " + row["time"], "%Y-%m-%d %H:%M")
    except ValueError:
        return "bad date or time (want YYYY-MM-DD and HH:MM)"
    if when > datetime.now():
        return "date is in the future"
    try:
        amount = int(row["amount"])
    except ValueError:
        return "amount is not a whole number of rupees"
    if amount <= 0:
        return "amount must be above zero"
    return None

def load(path):
    amounts, bad, seen = [], [], set()
    with open(path, newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        missing = [c for c in COLUMNS if c not in (reader.fieldnames or [])]
        if missing:
            raise ValueError("missing columns: " + ", ".join(missing))
        for row in reader:
            reason = check(row, seen)
            if reason:
                bad.append((reader.line_num, reason))
            else:
                seen.add(row["id"].strip())
                amounts.append(int(row["amount"]))
    return amounts, bad

def handed_over(amount, note):
    """Least money that covers the bill using only this note."""
    return -(-amount // note) * note

def make_change(value):
    out = Counter()
    for coin in CHANGE:
        out[coin], value = divmod(value, coin)
    return +out

def change_needed(amounts, note):
    total = Counter()
    for a in amounts:
        total += make_change(handed_over(a, note) - a)
    return total

def main(path="data.csv"):
    try:
        amounts, bad = load(path)
    except (OSError, ValueError) as e:
        print("Cannot read data:", e)
        return 1
    for line, reason in bad:
        print(f"Skipped line {line}: {reason}")
    print(f"Usable bills: {len(amounts)}")
    if len(amounts) < MIN_ROWS:
        print(f"Need at least {MIN_ROWS} usable bills for a suggestion.")
        return 1
    print(f"\nChange to keep per {PLAN_FOR} bills, if all pay with one kind of note:")
    worst = Counter()
    for note in NOTES:
        need = change_needed(amounts, note)
        plan = {c: -(-n * PLAN_FOR // len(amounts)) for c, n in need.items()}
        for c, n in plan.items():
            worst[c] = max(worst[c], n)
        print(f"  Rs {note}: " + ", ".join(f"{plan[c]} x Rs {c}" for c in CHANGE if c in plan))
    print("\nKeep ready: " + (", ".join(f"{worst[c]} x Rs {c}" for c in CHANGE if c in worst)
                             or "no change needed"))
    return 0

if __name__ == "__main__":
    sys.exit(main(*sys.argv[1:2]))
