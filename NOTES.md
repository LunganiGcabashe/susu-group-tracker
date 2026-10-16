# Notes: assumptions and design decisions

## Assumptions

1. A member is identified by a name or ID. Leading/trailing spaces are removed and uniqueness is case-insensitive.
2. Members may be added only before any contribution is recorded. Once contributions start in week 1, membership is frozen so the pot size and rotation order do not change.
3. Each member must contribute the fixed weekly amount. Partial payments are allowed and accumulate during the current week.
4. A week cannot close while any member owes money. An unsuccessful close does not advance the week or create a payout.
5. The payout amount is the fixed weekly contribution multiplied by the number of members.
6. Payouts follow joining order, one member per successfully closed week, then repeat from the first member.
7. Monetary values must be positive and have at most two decimal places. Python `Decimal` is used instead of binary floating-point arithmetic.
8. This program manages one group in memory. Data is not saved after the program exits.

## Design

The `SusuGroup` class contains the core rules so that the command-line interface remains simple and the rules can be tested independently. The tests use Python's built-in `unittest` framework.

## What I would improve with more time

- Save and load group data so it survives application restarts.
- Use persistent member IDs and validate them separately from display names.
- Add dates and timestamps to contributions and payout records.
- Add more tests for malformed input, whitespace, and boundary cases.
- Add structured logging and clearer error types.
- Consider a database-backed version if multiple users needed to access the group.
