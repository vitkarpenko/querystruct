import pytest

from querystruct import Querystruct


@pytest.mark.parametrize("query, expected", [
    ('{"status":"A"}', '(status = "A")'),
    ('{"age":{"$gt":"25","$lte":"50"}}', '((age > 25) AND (age <= 50))')
])
def test_to_sql(query, expected):
    assert Querystruct(query).to_sql() == expected
