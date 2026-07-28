import pandas as pd
import pytest

from quality.validator import DataValidator


class TestDataValidator:

    def test_validate_dataframe_success(self):
        """
        Test validation passes for a valid DataFrame.
        """

        df = pd.DataFrame(
            {
                "id": [1],
                "price": [100],
                "rating": [4.5],
            }
        )

        DataValidator.validate_dataframe(df)

    def test_validate_dataframe_empty(self):
        """
        Test empty DataFrame raises ValueError.
        """

        df = pd.DataFrame()

        with pytest.raises(ValueError):
            DataValidator.validate_dataframe(df)

    def test_duplicate_ids(self):
        """
        Test duplicate IDs raise ValueError.
        """

        df = pd.DataFrame(
            {
                "id": [1, 1],
                "price": [100, 200],
                "rating": [4.5, 4.0],
            }
        )

        with pytest.raises(ValueError):
            DataValidator.validate_duplicate_ids(df)

    def test_unique_ids(self):
        """
        Test unique IDs pass validation.
        """

        df = pd.DataFrame(
            {
                "id": [1, 2],
                "price": [100, 200],
                "rating": [4.5, 4.0],
            }
        )

        DataValidator.validate_duplicate_ids(df)

    def test_invalid_price(self):
        """
        Test negative price raises ValueError.
        """

        df = pd.DataFrame(
            {
                "id": [1],
                "price": [-100],
                "rating": [4.5],
            }
        )

        with pytest.raises(ValueError):
            DataValidator.validate_price(df)

    def test_valid_price(self):
        """
        Test positive price passes validation.
        """

        df = pd.DataFrame(
            {
                "id": [1],
                "price": [100],
                "rating": [4.5],
            }
        )

        DataValidator.validate_price(df)

    def test_invalid_rating_above_range(self):
        """
        Test rating greater than 5 raises ValueError.
        """

        df = pd.DataFrame(
            {
                "id": [1],
                "price": [100],
                "rating": [5.5],
            }
        )

        with pytest.raises(ValueError):
            DataValidator.validate_rating(df)

    def test_invalid_rating_below_range(self):
        """
        Test rating below 0 raises ValueError.
        """

        df = pd.DataFrame(
            {
                "id": [1],
                "price": [100],
                "rating": [-1],
            }
        )

        with pytest.raises(ValueError):
            DataValidator.validate_rating(df)

    def test_valid_rating(self):
        """
        Test valid rating passes validation.
        """

        df = pd.DataFrame(
            {
                "id": [1],
                "price": [100],
                "rating": [4.8],
            }
        )

        DataValidator.validate_rating(df)