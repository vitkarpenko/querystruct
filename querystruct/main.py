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
        self.query = json.load(querystruct)
        self.validate()

    def validate(self):
        pass

    def to_sql(self):
        """ По self.query генерирует WHERE часть соответствующего SQL SELECT запроса.

        Примеры:
        {'status':'A'} --> 'status = "A"'
        {'age':{'$gt':'25','$lte':'50'}} --> 'age > 25 AND age <= 50'
        """
        pass


