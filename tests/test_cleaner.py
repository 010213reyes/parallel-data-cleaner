import unittest
import pandas as pd

from src.cleaner import clean_dataframe


class TestCleaner(unittest.TestCase):

    def test_basic_cleaning(self):

        df = pd.DataFrame({
            "nombre": [
                " Ana  Maria ",
                "Ana Maria",
                "Luis",
                "Pedro"
            ],
            "edad": [25, 25, 30, None],
            "ciudad": ["México", "México", "N/A", "Guadalajara"]
        })

        cleaned, stats = clean_dataframe(df)

        self.assertEqual(len(cleaned), 3)
        self.assertEqual(stats["duplicates_removed"], 1)
        self.assertEqual(stats["original_nulls"], 1)
        self.assertEqual(stats["final_nulls"], 2)
        self.assertEqual(cleaned.iloc[0]["nombre"], "Ana Maria")
        self.assertTrue(pd.isna(cleaned.iloc[1]["ciudad"]))


if __name__ == "__main__":
    unittest.main()