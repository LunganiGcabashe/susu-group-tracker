"""Simple command-line interface for the susu group tracker."""

from decimal import Decimal, InvalidOperation
from .group import SusuGroup, format_money


def read_amount(prompt: str) -> Decimal:
    while True:
        raw = input(prompt).strip()
        try:
            amount = Decimal(raw)
            if not amount.is_finite():
                raise InvalidOperation
            return amount
        except (InvalidOperation, ValueError):
            print("Please enter a valid amount, for example 50.00.")


def show_report(group: SusuGroup) -> None:
    report = group.report()
    print(f"\n--- Week {report['current_week']} report ---")
    print(f"Weekly contribution: GHS {format_money(report['weekly_contribution'])}")
    if not report["members"]:
        print("No members have been added yet.")
    else:
        print("Member payments:")
        for member in report["members"]:
            paid = group.weekly_payments[member]
            owed = report["owing"].get(member, Decimal("0.00"))
            status = "Paid in full" if owed == 0 else f"Owes GHS {format_money(owed)}"
            print(f"  {member}: paid GHS {format_money(paid)} — {status}")

    print("Payout history:")
    if not report["payout_history"]:
        print("  No payouts yet.")
    else:
        for payout in report["payout_history"]:
            print(
                f"  Week {payout['week']}: {payout['recipient']} received "
                f"GHS {format_money(payout['amount'])}"
            )


def run() -> None:
    print("Welcome to Susu Group Tracker")
    while True:
        weekly = read_amount("Enter the fixed weekly contribution in GHS (e.g. 50.00): ")
        try:
            group = SusuGroup(weekly)
            break
        except ValueError as error:
            print(error)

    while True:
        print(
            "\n1. Add member\n"
            "2. Record contribution\n"
            "3. Close current week\n"
            "4. Show report\n"
            "5. Exit"
        )
        choice = input("Choose an option: ").strip()

        try:
            if choice == "1":
                name = input("Enter member name or ID: ")
                group.add_member(name)
                print(f"Added member: {name.strip()}")

            elif choice == "2":
                name = input("Enter member name or ID: ")
                amount = read_amount("Enter contribution amount in GHS: ")
                group.record_contribution(name, amount)
                print(f"Contribution recorded for {name.strip()}.")

            elif choice == "3":
                result = group.close_week()
                print(result["message"])
                if not result["closed"]:
                    for member, owed in result["owing"].items():
                        print(f"  {member} owes GHS {format_money(owed)}")

            elif choice == "4":
                show_report(group)

            elif choice == "5":
                print("Goodbye.")
                break

            else:
                print("Choose a number from 1 to 5.")

        except ValueError as error:
            print(f"Error: {error}")


if __name__ == "__main__":
    run()
