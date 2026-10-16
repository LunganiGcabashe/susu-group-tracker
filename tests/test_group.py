import unittest
from decimal import Decimal

from susu_tracker.group import SusuGroup


class SusuGroupTests(unittest.TestCase):
    def setUp(self):
        self.group = SusuGroup("50.00")
        self.group.add_member("Ama")
        self.group.add_member("Kofi")
        self.group.add_member("Esi")

    def test_add_member(self):
        self.group.add_member("Yaw")
        self.assertIn("Yaw", self.group.members)

    def test_duplicate_member_is_rejected_case_insensitively(self):
        with self.assertRaises(ValueError):
            self.group.add_member(" ama ")

    def test_unknown_member_is_rejected(self):
        with self.assertRaises(ValueError):
            self.group.record_contribution("Kojo", "10.00")

    def test_zero_and_negative_payments_are_rejected(self):
        for amount in ("0", "-1.00"):
            with self.subTest(amount=amount):
                with self.assertRaises(ValueError):
                    self.group.record_contribution("Ama", amount)

    def test_payment_above_outstanding_balance_is_rejected(self):
        self.group.record_contribution("Ama", "40.00")
        with self.assertRaises(ValueError):
            self.group.record_contribution("Ama", "10.01")

    def test_partial_payments_accumulate(self):
        self.group.record_contribution("Esi", "30.00")
        self.group.record_contribution("Esi", "20.00")
        self.assertEqual(self.group.weekly_payments["Esi"], Decimal("50.00"))

    def test_week_cannot_close_when_member_still_owes(self):
        self.group.record_contribution("Ama", "50.00")
        self.group.record_contribution("Kofi", "50.00")
        self.group.record_contribution("Esi", "30.00")

        result = self.group.close_week()

        self.assertFalse(result["closed"])
        self.assertEqual(result["owing"], {"Esi": Decimal("20.00")})
        self.assertEqual(self.group.current_week, 1)
        self.assertEqual(len(self.group.payout_history), 0)
