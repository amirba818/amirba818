import unittest
import math
from calculator import (
    add, subtract, multiply, divide,
    power, square_root, log10,
    sine, cosine, tangent
)

class TestCalculatorFunctions(unittest.TestCase):

    def test_add(self):
        self.assertEqual(add(1, 2), 3)
        self.assertEqual(add(-1, 1), 0)
        self.assertEqual(add(-1, -1), -2)
        self.assertEqual(add(0, 0), 0)
        self.assertAlmostEqual(add(0.1, 0.2), 0.3)

    def test_subtract(self):
        self.assertEqual(subtract(10, 5), 5)
        self.assertEqual(subtract(-1, 1), -2)
        self.assertEqual(subtract(-1, -1), 0)
        self.assertEqual(subtract(5, 10), -5)
        self.assertAlmostEqual(subtract(0.3, 0.1), 0.2)

    def test_multiply(self):
        self.assertEqual(multiply(3, 5), 15)
        self.assertEqual(multiply(-1, 1), -1)
        self.assertEqual(multiply(-1, -1), 1)
        self.assertEqual(multiply(5, 0), 0)
        self.assertAlmostEqual(multiply(0.5, 0.5), 0.25)

    def test_divide(self):
        self.assertEqual(divide(10, 2), 5)
        self.assertEqual(divide(-10, 2), -5)
        self.assertEqual(divide(10, -2), -5)
        self.assertEqual(divide(-10, -2), 5)
        self.assertAlmostEqual(divide(1, 3), 0.3333333333333333)
        self.assertEqual(divide(0, 5), 0)
        # Test division by zero
        self.assertEqual(divide(10, 0), "خطا: تقسیم بر صفر امکان‌پذیر نیست.")

    def test_power(self):
        self.assertEqual(power(2, 3), 8)
        self.assertEqual(power(5, 0), 1)
        self.assertEqual(power(0, 5), 0) # 0 to any positive power is 0
        self.assertEqual(power(2, -2), 0.25)
        self.assertAlmostEqual(power(4, 0.5), 2) # Square root

    def test_square_root(self):
        self.assertEqual(square_root(9), 3)
        self.assertEqual(square_root(0), 0)
        self.assertAlmostEqual(square_root(2), 1.4142135623730951)
        # Test negative input
        self.assertEqual(square_root(-4), "خطا: جذر عدد منفی تعریف نشده است (در اعداد حقیقی).")

    def test_log10(self):
        self.assertEqual(log10(100), 2)
        self.assertEqual(log10(1), 0)
        self.assertAlmostEqual(log10(50), 1.6989700043360187)
        # Test non-positive input
        self.assertEqual(log10(0), "خطا: لگاریتم برای اعداد غیر مثبت تعریف نشده است.")
        self.assertEqual(log10(-10), "خطا: لگاریتم برای اعداد غیر مثبت تعریف نشده است.")

    def test_sine(self):
        self.assertAlmostEqual(sine(0), 0)
        self.assertAlmostEqual(sine(30), 0.5)
        self.assertAlmostEqual(sine(90), 1)
        self.assertAlmostEqual(sine(180), 0)
        self.assertAlmostEqual(sine(270), -1)
        self.assertAlmostEqual(sine(360), 0)
        self.assertAlmostEqual(sine(45), math.sin(math.radians(45)))

    def test_cosine(self):
        self.assertAlmostEqual(cosine(0), 1)
        self.assertAlmostEqual(cosine(60), 0.5)
        self.assertAlmostEqual(cosine(90), 0)
        self.assertAlmostEqual(cosine(180), -1)
        self.assertAlmostEqual(cosine(270), 0)
        self.assertAlmostEqual(cosine(360), 1)
        self.assertAlmostEqual(cosine(45), math.cos(math.radians(45)))

    def test_tangent(self):
        self.assertAlmostEqual(tangent(0), 0)
        self.assertAlmostEqual(tangent(45), 1)
        self.assertAlmostEqual(tangent(180), 0)
        self.assertAlmostEqual(tangent(360), 0)
        # Test undefined cases
        self.assertEqual(tangent(90), "خطا: تانژانت برای این زاویه تعریف نشده است.")
        self.assertEqual(tangent(270), "خطا: تانژانت برای این زاویه تعریف نشده است.")
        self.assertAlmostEqual(tangent(30), math.tan(math.radians(30)))

if __name__ == '__main__':
    unittest.main()
