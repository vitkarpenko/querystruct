import json

from .utils import isnumber


class Querystruct:
    """ Реализует валидацию и трансляцию в SQL mongo-like языка запросов.

    self.query: словарь, полученный десериализацией json'a, представляющего запрос.

    Пример использования:
        query = Querystruct('{"age":{"$lt":"25"}}') # парсинг json'a и валидация
        query.to_sql()

    """
    comparison_operators = {
        '$lt': '<',
        '$lte': '<=',
        '$gt': '>',
        '$gte': '>=',
        '$ne': '!='
    }

    def __init__(self, querystruct):
        """ querystruct: сериализованный json """
        self.query = json.loads(querystruct)
        print(querystruct)
        print(self.query)
        self.validate()

    def validate(self):
        pass

    def to_sql(self, query=None, parents=None):
        """ По self.query рекурсивно генерирует WHERE часть соответствующего SQL SELECT запроса.

        parents: список всех ключей выше по "дереву" запроса вплоть до текущего.

        В силу своей рекурсивности генерирует "лишние" скобки, но это не имеет значения,
        т.к. результат в целом не предназначен для чтения человеком.

        Примеры:
        {'status':'A'} -> "(status = 'A')"
        {'age':{'$gt':'25','$lte':'50'}} -> "((age > 25) AND (age <= 50))"
        """
        if not query:
            query = self.query
        if not parents:
            parents = ['']

        if parents[-1] in self.comparison_operators:
            value = query if isnumber(query) else f"'{query}'"
            return f"{parents[-2]} {self.comparison_operators[parents[-1]]} {value}"

        if not parents[-1].startswith('$'):
            if isinstance(query, str):
                value = query if isnumber(query) else f"'{query}'"
                return f"{parents[-1]} = {value}"

        if parents[-1].startswith('$or'):
            return ' OR '.join(
                self.to_sql(querypart)
                for querypart in query
            )

        return ' AND '.join(
            '(' + self.to_sql(querypart, parents + [parent]) + ')'
            for parent, querypart in query.items()
        )
