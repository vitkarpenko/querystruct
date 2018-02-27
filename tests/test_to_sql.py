import pytest

from querystruct import Querystruct


@pytest.mark.parametrize("query, expected", [
    ('{"status": "A"}', "(status = 'A')"),
    ('{"value": "100500"}', "(value = 100500)"),
    ('{"rabbit": {"$ne": "mq"}}', "((rabbit != 'mq'))"),
    ('{"age": {"$gt": "25"}}', '((age > 25))'),
    ('{"age": {"$gt": "25", "$lte": "50"}}', '((age > 25) AND (age <= 50))'),
    ('{"$or": [{"beer": "meh"}, {"beer": "gut"}]}', "((beer = 'meh') OR (beer = 'gut'))"),
    ('{"$or": [{"beer": "meh"}, {"beer_price": {"$lt": "50"}}]}', "((beer = 'meh') OR ((beer_price < 50)))"),
    ('{"bloodbourne": "meh", "diabloIII": "gut"}', "(bloodbourne = 'meh') AND (diabloIII = 'gut')")
])
def test_to_sql(query, expected):
    assert Querystruct(query).to_sql() == expected
