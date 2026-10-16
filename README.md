# Susu Group Tracker

A small Python command-line application for managing one rotating savings group (susu).

## Features

- Set a fixed weekly contribution in GHS.
- Add uniquely named members.
- Record full or partial contributions for the current week.
- Prevent invalid payments and overpayments.
- Close a week only after every member has paid in full.
- Pay the pot to the next member in joining order.
- Show current-week payment status, outstanding balances, and payout history.
- Use `Decimal` for exact monetary arithmetic.

## Requirements

- Python 3.10 or newer recommended.
- Git is needed if you want to work with the repository history.

## Run the application

From the project root:

```bash
python -m susu_tracker
```

## Run automated tests

From the project root, run:

```bash
python -m unittest discover -s tests -v
```

The tests use Python's built-in `unittest` framework; no third-party test package is required.

## Example workflow

1. Start the application and enter `50.00` as the weekly contribution.
2. Add Ama, Kofi and Esi.
3. Record GHS 50.00 for Ama and Kofi, and GHS 30.00 for Esi.
4. Close the week. The week stays open and reports that Esi owes GHS 20.00.
5. Record Esi's remaining GHS 20.00 and close the week again.
6. Ama receives GHS 150.00, and week 2 begins.

## Project structure

- `susu_tracker/group.py`: core business rules.
- `susu_tracker/cli.py`: command-line menu.
- `tests/test_group.py`: automated tests.
- `NOTES.md`: assumptions and possible improvements.
