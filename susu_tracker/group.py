"""Core business rules for a rotating susu savings group."""

from decimal import Decimal, InvalidOperation
from typing import Dict, List


def money(value) -> Decimal:
    """Convert a value to a two-decimal-place Decimal, rejecting invalid money."""
    try:
        amount = value if isinstance(value, Decimal) else Decimal(str(value).strip())
    except (InvalidOperation, ValueError, AttributeError):
        raise ValueError("Enter a valid monetary amount.") from None

    if not amount.is_finite():
        raise ValueError("Amount must be a finite number.")
    if amount <= 0:
        raise ValueError("Amount must be greater than zero.")
    if amount != amount.quantize(Decimal("0.01")):
        raise ValueError("Amounts may have no more than two decimal places.")
    return amount.quantize(Decimal("0.01"))


def format_money(amount: Decimal) -> str:
    """Format a Decimal as a two-decimal-place amount."""
    return f"{amount:.2f}"


class SusuGroup:
    """Manage members, weekly contributions, week closure, and payouts."""

    def __init__(self, weekly_contribution):
        self.weekly_contribution = money(weekly_contribution)
        self.members: List[str] = []
        self.current_week = 1
        self.weekly_payments: Dict[str, Decimal] = {}
        self.payout_history: List[dict] = []
        self._member_keys = set()
        self._contributions_started = False

    def add_member(self, name: str) -> None:
        if not isinstance(name, str) or not name.strip():
            raise ValueError("Member name or ID cannot be empty.")

        cleaned_name = name.strip()
        key = cleaned_name.casefold()
        if key in self._member_keys:
            raise ValueError(f"Member '{cleaned_name}' already exists.")
        if self.current_week != 1 or self._contributions_started:
            raise ValueError("Members cannot be added after week 1 has started.")

        self.members.append(cleaned_name)
        self._member_keys.add(key)
        self.weekly_payments[cleaned_name] = Decimal("0.00")

    def record_contribution(self, member_name: str, amount) -> None:
        member = self._find_member(member_name)
        payment = money(amount)
        already_paid = self.weekly_payments[member]
        outstanding = self.weekly_contribution - already_paid

        if payment > outstanding:
            raise ValueError(
                f"Payment exceeds the outstanding balance of {format_money(outstanding)}."
            )

        self.weekly_payments[member] = already_paid + payment
        self._contributions_started = True

    def close_week(self) -> dict:
        if not self.members:
            raise ValueError("Add at least one member before closing a week.")

        owing = self.outstanding_balances()
        if owing:
            return {
                "closed": False,
                "week": self.current_week,
                "owing": owing,
                "message": "Week cannot close because some members still owe money.",
            }

        payout_amount = self.weekly_contribution * len(self.members)
        recipient_index = len(self.payout_history) % len(self.members)
        recipient = self.members[recipient_index]
        payout = {
            "week": self.current_week,
            "recipient": recipient,
            "amount": payout_amount,
        }
        self.payout_history.append(payout)

        closed_week = self.current_week
        self.current_week += 1
        self.weekly_payments = {
            member: Decimal("0.00") for member in self.members
        }
        return {
            "closed": True,
            "week": closed_week,
            "payout": payout,
            "message": (
                f"Week {closed_week} closed. {recipient} receives "
                f"GHS {format_money(payout_amount)}."
            ),
        }

    def outstanding_balances(self) -> dict:
        return {
            member: self.weekly_contribution - self.weekly_payments[member]
            for member in self.members
            if self.weekly_payments[member] < self.weekly_contribution
        }

    def report(self) -> dict:
        paid_in_full = [
            member for member in self.members
            if self.weekly_payments[member] == self.weekly_contribution
        ]
        return {
            "current_week": self.current_week,
            "weekly_contribution": self.weekly_contribution,
            "members": list(self.members),
            "paid_in_full": paid_in_full,
            "owing": self.outstanding_balances(),
            "payout_history": list(self.payout_history),
        }

    def _find_member(self, member_name: str) -> str:
        if not isinstance(member_name, str):
            raise ValueError("Unknown member.")
        key = member_name.strip().casefold()
        for member in self.members:
            if member.casefold() == key:
                return member
        raise ValueError(f"Unknown member '{member_name}'.")
