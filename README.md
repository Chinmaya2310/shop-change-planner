# Shop change planner
Suggests which coins and notes a shop should keep ready.

Intended for: small general stores. One shopkeeper, Rajeev Gupta, said he has
this problem (gist from memory). No timed visit was done.
Data: 21 real payments, 24 Aug to 23 Nov 2026; shop or shops not specified.

## Run
    python3 tool.py
    python3 drawer.py 200x2,100x2,50x3,20x5,10x5,5x4
    python3 test_tool.py

## Output on data.csv
```
Usable bills: 21

Change to keep per 10 bills, if all pay with one kind of note:
  Rs 50: 11 x Rs 20, 5 x Rs 10, 2 x Rs 5
  Rs 100: 7 x Rs 50, 11 x Rs 20, 5 x Rs 10, 2 x Rs 5
  Rs 500: 20 x Rs 200, 7 x Rs 50, 11 x Rs 20, 5 x Rs 10, 2 x Rs 5

Keep ready: 20 x Rs 200, 7 x Rs 50, 11 x Rs 20, 5 x Rs 10, 2 x Rs 5
```

All 21 bills are multiples of Rs 5, so the tool never suggests Rs 1 or Rs 2 coins.
This may not hold for any real shop.

## How long a drawer lasts
The drawer below is an example, not a real shop's cash. Bills run in data.csv order.
```
All pay with Rs 50: 7 bills served, then cannot give Rs 40
All pay with Rs 100: 4 bills served, then cannot give Rs 90
All pay with Rs 500: 1 bills served, then cannot give Rs 460
```

## What it gets wrong
- The rows are 21 payments, not a shop's full sales records.
- A UPI bill may differ from what people buy with cash.
- It assumes everyone pays with one kind of note and never offers coins.
- tool.py ignores notes that come in from customers. drawer.py reuses them, but assumes
  every customer pays with the same kind of note and runs bills in data.csv order.
- No shopkeeper has tried it.

Video: not recorded
