import json

from .utils import (
    isnumber,
    format_sql_value    
)


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
        '$gte': '>='
    }

    def __init__(self, querystruct):
        """ querystruct: сериализованный json """
        self.query = json.loads(querystruct)
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
        # query может быть None в процессе выполнения метода
        # -> для корня нужно проверять так же и parents
        if not query and not parents:
            query = self.query
        # пустая строка представляет корень
        if not parents:
            parents = ['']

        if parents[-1] in self.comparison_operators:
            return f"{parents[-2]} {self.comparison_operators[parents[-1]]} {format_sql_value(query)}"

        if parents[-1].startswith('$ne'):
            if query is None:
                return f"{parents[-2]} IS NOT {format_sql_value(query)}"
            elif not isinstance(query, dict):
                return f"{parents[-2]} != {format_sql_value(query)}"

        if parents[-1].startswith('$in'):
            return f"{parents[-2]} IN ({', '.join(format_sql_value(value) for value in query)})"

        if parents[-1].startswith('$or'):
            return ' OR '.join(
                self.to_sql(querypart)
                for querypart in query
            )

        if not parents[-1].startswith('$'):
            if query is None:
                return f"{parents[-1]} IS {format_sql_value(query)}"
            elif not isinstance(query, dict):
                return f"{parents[-1]} = {format_sql_value(query)}"

        return ' AND '.join(
            '(' + self.to_sql(querypart, parents + [parent]) + ')'
            for parent, querypart in query.items()
        )
