import pandas as pd

from services.silver_to_gold import SilverToGoldService


class TestSilverToGoldService:

    def setup_method(self):
        """
        Create service instance for each test.
        """
        self.service = SilverToGoldService()

    def test_create_product_summary(self):
        """
        Test Gold summary aggregation.
        """

        df = pd.DataFrame(
            [
                {
                    "id": 1,
                    "category": "electronics",
                    "price": 100,
                    "rating": 4,
                    "review_count": 10,
                },
                {
                    "id": 2,
                    "category": "electronics",
                    "price": 200,
                    "rating": 5,
                    "review_count": 20,
                },
                {
                    "id": 3,
                    "category": "jewelery",
                    "price": 300,
                    "rating": 3,
                    "review_count": 30,
                },
            ]
        )

        result = self.service.create_product_summary(df)

        electronics = result[
            result["category"] == "electronics"
        ].iloc[0]

        assert electronics["total_products"] == 2
        assert electronics["average_price"] == 150
        assert electronics["min_price"] == 100
        assert electronics["max_price"] == 200
        assert electronics["average_rating"] == 4.5
        assert electronics["total_reviews"] == 30

    def test_summary_has_correct_categories(self):
        """
        Test category count.
        """

        df = pd.DataFrame(
            [
                {
                    "id": 1,
                    "category": "electronics",
                    "price": 100,
                    "rating": 4,
                    "review_count": 10,
                },
                {
                    "id": 2,
                    "category": "jewelery",
                    "price": 200,
                    "rating": 5,
                    "review_count": 20,
                },
            ]
        )

        result = self.service.create_product_summary(df)

        assert len(result) == 2

    def test_average_price_rounding(self):
        """
        Test average price is rounded.
        """

        df = pd.DataFrame(
            [
                {
                    "id": 1,
                    "category": "electronics",
                    "price": 100.11,
                    "rating": 4,
                    "review_count": 10,
                },
                {
                    "id": 2,
                    "category": "electronics",
                    "price": 100.22,
                    "rating": 5,
                    "review_count": 20,
                },
            ]
        )

        result = self.service.create_product_summary(df)

        value = result.iloc[0]["average_price"]

        assert value == round(value, 2)

    def test_total_reviews(self):
        """
        Test review aggregation.
        """

        df = pd.DataFrame(
            [
                {
                    "id": 1,
                    "category": "electronics",
                    "price": 100,
                    "rating": 4,
                    "review_count": 25,
                },
                {
                    "id": 2,
                    "category": "electronics",
                    "price": 150,
                    "rating": 5,
                    "review_count": 75,
                },
            ]
        )

        result = self.service.create_product_summary(df)

        assert result.iloc[0]["total_reviews"] == 100

    def test_output_columns(self):
        """
        Test expected Gold columns exist.
        """

        df = pd.DataFrame(
            [
                {
                    "id": 1,
                    "category": "electronics",
                    "price": 100,
                    "rating": 4,
                    "review_count": 10,
                }
            ]
        )

        result = self.service.create_product_summary(df)

        expected = {
            "category",
            "total_products",
            "average_price",
            "min_price",
            "max_price",
            "average_rating",
            "total_reviews",
        }

        assert expected.issubset(result.columns)