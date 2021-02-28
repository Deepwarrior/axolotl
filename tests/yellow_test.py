import unittest
from axol import why_yellow


class MyTestCase(unittest.TestCase):
    def test_primitive(self):
        text = "ЖОЛТ"
        actual = why_yellow(text)
        self.assertEqual(actual, "ДА ПОЧЕМУ ЖОЛТ-ТО")

    def test_zaborchik(self):
        text = "жОлТ"
        actual = why_yellow(text)
        self.assertEqual(actual, "ДА ПОЧЕМУ ЖОЛТ-ТО")

    def test_alphas_aroung(self):
        text = "ОЖОЖОЛТЫЙ"
        actual = why_yellow(text)
        self.assertEqual(actual, "ДА ПОЧЕМУ ОЖОЖОЛТЫЙ-ТО")

    def test_not_alphas_around(self):
        text = "!@#$ЖОЛТ1234"
        actual = why_yellow(text)
        self.assertEqual(actual, "ДА ПОЧЕМУ ЖОЛТ-ТО")

    def test_alphas_around_then_not_alphas(self):
        text = "!@#$ПОЖОЛТЕВШИЙ1234"
        actual = why_yellow(text)
        self.assertEqual(actual, "ДА ПОЧЕМУ ПОЖОЛТЕВШИЙ-ТО")

    def test_not_cyrillic_around(self):
        text = "ZZZЖОЛТZZZ"
        actual = why_yellow(text)
        self.assertEqual(actual, "ДА ПОЧЕМУ ЖОЛТ-ТО")

    def test_case_from_chat_1(self):
        text = "ЖОЛТ';SELECT password from users;--"
        actual = why_yellow(text)
        self.assertEqual(actual, "ДА ПОЧЕМУ ЖОЛТ-ТО")

    def test_case_from_chat_2(self):
        text = "Жолток жолтого жолторотика"
        yellows = ["ДА ПОЧЕМУ ЖОЛТОК-ТО", "ДА ПОЧЕМУ ЖОЛТОГО-ТО", "ДА ПОЧЕМУ ЖОЛТОРОТИКА-ТО"]
        for i in range(100):
            actual = why_yellow(text)
            self.assertTrue(actual in yellows)

    def test_case_from_chat_2_1(self):
        text = "Синий жолток маленького жолтого пингвина-жолторотика"
        yellows = ["ДА ПОЧЕМУ ЖОЛТОК-ТО", "ДА ПОЧЕМУ ЖОЛТОГО-ТО", "ДА ПОЧЕМУ ЖОЛТОРОТИКА-ТО"]
        for i in range(100):
            actual = why_yellow(text)
            self.assertTrue(actual in yellows)


if __name__ == '__main__':
    unittest.main()
