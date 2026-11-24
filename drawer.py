"""Given the cash in the drawer now, find which bill it first fails to give change for.

Example: python3 drawer.py 200x2,100x2,50x3,20x5,10x5,5x4
"""
import sys
from collections import Counter
import tool

def parse(text):
    """Turn 50x3,20x5 into {50: 3, 20: 5}."""
    drawer = Counter()
    for part in text.split(","):
        value, count = (int(x) for x in part.lower().split("x"))
        if value not in tool.CHANGE + [500] or count < 0:
            raise ValueError(part)
        drawer[value] += count
    return drawer

def pay(value, drawer, coins=tool.CHANGE):
    """Find change using only what is in the drawer, or None."""
    if value == 0:
        return Counter()
    if not coins:
        return None
    coin, rest = coins[0], coins[1:]
    for n in range(min(value // coin, drawer[coin]), -1, -1):
        found = pay(value - n * coin, drawer, rest)
        if found is not None:
            found[coin] += n
            return found
    return None

def replay(amounts, note, start):
    """Serve bills in order. Return (bills served, change that failed or None)."""
    drawer = Counter(start)
    for i, amount in enumerate(amounts):
        given = tool.handed_over(amount, note)
        drawer[note] += given // note      # the customer's notes go in first
        change = pay(given - amount, drawer)
        if change is None:
            return i, given - amount
        drawer -= change
    return len(amounts), None

def main(args):
    try:
        drawer = parse(args[0])
    except (IndexError, ValueError):
        print("Give the drawer like this: python3 drawer.py 200x2,50x3,20x5,10x5,5x4")
        return 1
    try:
        amounts, bad = tool.load(args[1] if len(args) > 1 else "data.csv")
    except (OSError, ValueError) as e:
        print("Cannot read data:", e)
        return 1
    for line, reason in bad:
        print(f"Skipped line {line}: {reason}")
    if len(amounts) < tool.MIN_ROWS:
        print(f"Need at least {tool.MIN_ROWS} usable bills.")
        return 1
    for note in tool.NOTES:
        served, short = replay(amounts, note, drawer)
        if short is None:
            print(f"All pay with Rs {note}: drawer lasts all {served} bills")
        else:
            print(f"All pay with Rs {note}: {served} bills served, then cannot give Rs {short}")
    return 0

if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
