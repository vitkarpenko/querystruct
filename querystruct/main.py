import json


class Querystruct:
    """ Реализует валидацию и трансляцию в SQL mongo-like языка запросов.

    self.query: словарь, полученный десериализацией json'a, представляющего запрос.

    Пример использования:
        query = Querystruct('{"age":{"$lt":"25"}}') # парсинг json'a и валидация
        query.to_sql()

    """

    def __init__(self, querystruct):
        """ querystruct: сериализованный json """
        self.query = json.loads(querystruct)
        self.validate()

    def validate(self):
        pass

    def to_sql(self, query=None, parent=None):
        """ По self.query рекурсивно генерирует WHERE часть соответствующего SQL SELECT запроса.

        parent: 

        Примеры:
        {'status':'A'} --> '(status = "A")'
        {'age':{'$gt':'25','$lte':'50'}} --> ('age > 25 AND age <= 50')
        """
        if not query:
            query = self.query

        if parent == None:
            return ' AND '.join(
                '(' + self.to_sql(querypart, parent) + ')'
                for parent, querypart in query.items()
            )
        elif parent.startswith('$or'):
            return ' OR '.join(
                '(' + self.to_sql(querypart, parent) + ')'
                for parent, querypart in query.items()
            )
        elif not parent.startswith('$'):
            if isinstance(query, str):
                return f'{parent} = "{query}"'
