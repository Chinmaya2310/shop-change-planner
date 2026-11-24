# Shop change planner
Suggests which coins and notes a shop should keep ready.

**Practice project. No fieldwork was done. The 21 bill amounts are real payments; the shop or shops are not specified.**

## Example user (fictional)
Rajeev is an invented general store owner, used to explain the tool. No visit or interview took place.
A customer hands him Rs 500 for a Rs 35 bill, then another does the same, and his Rs 200 and Rs 50
notes run out first. The tool reads past bill amounts and suggests what to keep ready.

## Run
    python3 tool.py
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

## What it gets wrong
- The rows are 21 payments, not a shop's full sales records.
- A UPI bill may differ from what people buy with cash.
- It assumes everyone pays with one kind of note and never offers coins.
- It ignores change that comes in from customers during the day.
- It has not been checked with any shopkeeper.

Video: not recorded
