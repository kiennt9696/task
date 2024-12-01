import unittest
from unittest.mock import patch, MagicMock
from datetime import datetime
from helpers.util import get_current_user, parse_sort_query, convert_str2time


class TestUtilityFunctions(unittest.TestCase):

    @patch("jwt.decode")
    def test_get_current_user(self, mock_jwt_decode):
        mock_token = "test_token"
        mock_public_key = "test_public_key"
        expected_user = {"username": "test_user"}

        mock_jwt_decode.return_value = expected_user

        result = get_current_user(mock_token, mock_public_key)

        self.assertEqual(result, expected_user)
        mock_jwt_decode.assert_called_once_with(
            mock_token,
            mock_public_key.encode(),
            algorithms="RS256",
            options={"verify_aud": False},
        )

    def test_parse_sort_query(self):
        class MockModel:
            field1 = MagicMock()
            field2 = MagicMock()

        sort_query = "-field1,field2"
        result = parse_sort_query(MockModel, sort_query)

        self.assertEqual(len(result), 2)

    def test_parse_sort_query_invalid_field(self):
        class MockModel:
            valid_field = MagicMock()

        sort_query = "-invalid_field,valid_field"
        result = parse_sort_query(MockModel, sort_query)

        self.assertEqual(len(result), 1)
        self.assertFalse(result[0].desc.called)

    def test_convert_str2time(self):
        time_str = "2023-11-30 12:00:00"
        expected_time = datetime(2023, 11, 30, 12, 0, 0)

        result = convert_str2time(time_str)

        self.assertEqual(result, expected_time)

    def test_convert_str2time_invalid_format(self):
        time_str = "30-11-2023 12:00:00"
        with self.assertRaises(ValueError):
            convert_str2time(time_str)
