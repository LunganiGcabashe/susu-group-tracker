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
