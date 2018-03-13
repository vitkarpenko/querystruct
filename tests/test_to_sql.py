import pytest

from querystruct import Querystruct


@pytest.mark.parametrize("query, expected", [
    (
        {"status": "A"},
        "(status = 'A')"
    ),
    (
        {"value": "100500"},
        "(value = 100500)"
    ),
    (
        {"value": 100500},
        "(value = 100500)"
    ),
    (
        {"value": 100.5},
        "(value = 100.5)"
    ),
    (
        {"value": None},
        "(value IS NULL)"
    ),
    (
        {"rabbit": {"$ne": "mq"}},
        "((rabbit != 'mq'))"
    ),
    (
        {"rabbit": {"$ne": None}},
        "((rabbit IS NOT NULL))"
    ),
    (
        {"age": {"$gt": "25"}},
        '((age > 25))'
    ),
    (
        {"age": {"$gt": "25", "$lte": "50"}},
        '((age > 25) AND (age <= 50))'
    ),
    (
        {"$or": [{"beer": "meh"}, {"beer": "gut"}]},
        "((beer = 'meh') OR (beer = 'gut'))"
    ),
    (
        {"$or": [{"beer": "atollius"}, {"beer_price": {"$lt": "50", "$gte": "20"}}]},
        "((beer = 'atollius') OR ((beer_price < 50) AND (beer_price >= 20)))"
    ),
    (
        {"bloodbourne": "meh", "diabloIII": "gut"},
        "(bloodbourne = 'meh') AND (diabloIII = 'gut')"
    ),
    (
        {"$or": [{"language": {"$in": ["python", "haskell", "go"]}}, {"free_beer": True}]},
        "(((language IN ('python', 'haskell', 'go'))) OR (free_beer = TRUE))"
    ),
    (
        {"language": {"$in": ["javascript", "perl"]}, "life": "pain"},
        "((language IN ('javascript', 'perl'))) AND (life = 'pain')"
    )
])
def test_to_sql(query, expected):
    assert Querystruct(query).to_sql() == expected
