import pytest

from querystruct import Querystruct


@pytest.mark.parametrize("query, expected", [
    ('{"status":"A"}', '(status = "A")')
])
def test_to_sql(query, expected):
    assert Querystruct(query).to_sql() == expected
