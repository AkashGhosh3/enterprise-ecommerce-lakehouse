import pandas as pd

from services.bronze_to_silver import BronzeToSilverService


class TestBronzeToSilverService:

    def setup_method(self):
        """
        Create service instance for each test.
        """
        self.service = BronzeToSilverService()

    def test_transform_flattens_rating(self):
        """
        Test nested rating dictionary is flattened correctly.
        """

        df = pd.DataFrame(
            [
                {
                    "id": 1,
                    "title": "Laptop",
                    "price": 999.99,
                    "category": "electronics",
                    "rating": {
                        "rate": 4.8,
                        "count": 120,
                    },
                }
            ]
        )

        result = self.service.transform(df)

        assert result.loc[0, "rating"] == 4.8
        assert result.loc[0, "review_count"] == 120

    def test_transform_removes_duplicates(self):
        """
        Test duplicate IDs are removed.
        """

        df = pd.DataFrame(
            [
                {
                    "id": 1,
                    "price": 100,
                    "rating": {
                        "rate": 4.0,
                        "count": 10,
                    },
                },
                {
                    "id": 1,
                    "price": 100,
                    "rating": {
                        "rate": 4.0,
                        "count": 10,
                    },
                },
                {
                    "id": 2,
                    "price": 200,
                    "rating": {
                        "rate": 5.0,
                        "count": 20,
                    },
                },
            ]
        )

        result = self.service.transform(df)

        assert len(result) == 2

        assert result["id"].tolist() == [1, 2]

    def test_transform_handles_missing_rating(self):
        """
        Test missing rating is replaced with zero.
        """

        df = pd.DataFrame(
            [
                {
                    "id": 1,
                    "price": 150,
                    "rating": None,
                }
            ]
        )

        result = self.service.transform(df)

        assert result.loc[0, "rating"] == 0
        assert result.loc[0, "review_count"] == 0

    def test_transform_contains_expected_columns(self):
        """
        Test transformed dataframe contains expected columns.
        """

        df = pd.DataFrame(
            [
                {
                    "id": 1,
                    "price": 100,
                    "rating": {
                        "rate": 4.5,
                        "count": 50,
                    },
                }
            ]
        )

        result = self.service.transform(df)

        expected_columns = {
            "id",
            "price",
            "rating",
            "review_count",
        }

        assert expected_columns.issubset(result.columns)

    def test_transform_keeps_dataframe_length(self):
        """
        Test dataframe length remains unchanged
        when there are no duplicates.
        """

        df = pd.DataFrame(
            [
                {
                    "id": 1,
                    "price": 100,
                    "rating": {
                        "rate": 4,
                        "count": 10,
                    },
                },
                {
                    "id": 2,
                    "price": 200,
                    "rating": {
                        "rate": 5,
                        "count": 20,
                    },
                },
            ]
        )

        result = self.service.transform(df)

        assert len(result) == 2

    def test_transform_fills_missing_review_count(self):
        """
        Test review_count defaults to zero.
        """

        df = pd.DataFrame(
            [
                {
                    "id": 1,
                    "price": 120,
                    "rating": {},
                }
            ]
        )

        result = self.service.transform(df)

        assert result.loc[0, "rating"] == 0
        assert result.loc[0, "review_count"] == 0