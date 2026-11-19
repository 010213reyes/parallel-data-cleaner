import unittest

import pandas as pd

from src.cleaner import clean_dataframe


class TestCleaner(unittest.TestCase):

    def test_basic_cleaning(self):

        df = pd.DataFrame({
            "nombre": [" Ana ", "Ana", "Luis", "Pedro"],
            "edad": [25, 25, 30, None],
        })

        cleaned, stats = clean_dataframe(df)

        self.assertEqual(len(cleaned), 3)

        self.assertEqual(
            stats["duplicates_removed"], 1
        )

        self.assertEqual(
            stats["null_values"], 1
        )

        self.assertEqual(
            cleaned.iloc[0]["nombre"], "Ana"
        )


if __name__ == "__main__":
    unittest.main()