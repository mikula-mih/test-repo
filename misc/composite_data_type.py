import random
from pympler import asizeof

def humanize_bytes(num, suffix='B'):
    """Formatting byte size into readable form"""
    for unit in ['', 'K', 'M', 'G', 'T', 'P', 'E', 'Z']:
        if abs(num) < 1024.0:
            return "%3.1f%s%s" % (num, unit, suffix)
        num /= 1024.0
    return "%.1f%s%s" % (num, 'Yi', suffix)


def list_of_dicts():
    many_dicts = []
    for i in range(1000):
        many_dicts.append({
            'city': '0c5b2444-70a0-4932-980c-b4dc0d3f02b5',
            'tariffs': [{
                'shop_id': random.randint(1, 10000),
                'delivery_days': random.randint(1, 12),
                'delivery_price': random.randint(125, 888),
            } for _ in range(3)]
        })
    print(f'List[Dict], mamory size: '
          f'{humanize_bytes(asizeof.asizeof(many_dicts))}')


def list_of_dataclass():
    from dataclasses import dataclass

    @dataclass
    class RecordDataClass:
        shop_id: int
        delivery_days: int
        delivery_price: int

    many_dataclasses = []
    for i in range(1000):
        many_dataclasses.append({
            'city': '0c5b2444-70a0-4932-980c-b4dc0d3f02b5',
            'tariffs': [
                RecordDataClass(
                    shop_id=random.randint(1, 10000),
                    delivery_days=random.randint(1, 12),
                    delivery_price=random.randint(125, 888)
                ) for _ in range(3)
            ]
        })
    print(f'List[Dataclass], mamory size: '
          f'{humanize_bytes(asizeof.asizeof(many_dataclasses))}')


def list_of_namedtuple():
    from collections import namedtuple

    Record = namedtuple('Record', 'shop_id delivery_days delivery_price')
    many_namedtuples = []
    for i in range(1000):
        many_namedtuples.append({
            'city': '0c5b2444-70a0-4932-980c-b4dc0d3f02b5',
            'tariffs': [
                Record(
                    shop_id=random.randint(1, 10000),
                    delivery_days=random.randint(1, 12),
                    delivery_price=random.randint(125, 888)
                ) for _ in range(3)
            ]
        })
    print(f'List[namedtuple], mamory size: '
          f'{humanize_bytes(asizeof.asizeof(many_namedtuples))}')


def list_of_namedtuple_inheritance():
    from typing import NamedTuple

    class RecordNamedTuple(NamedTuple):
        shop_id: int
        delivery_days: int
        delivery_price: int

    many_namedtuples2 = []
    for i in range(1000):
        many_namedtuples2.append({
            'city': '0c5b2444-70a0-4932-980c-b4dc0d3f02b5',
            'tariffs': [
                RecordNamedTuple(
                    shop_id=random.randint(1, 10000),
                    delivery_days=random.randint(1, 12),
                    delivery_price=random.randint(125, 888)
                ) for _ in range(3)
            ]
        })
    print(f'List[namedtuple2], mamory size: '
          f'{humanize_bytes(asizeof.asizeof(many_namedtuples2))}')


def best_case():
    from dataclasses import dataclass
    from typing import NamedTuple, Tuple

    class RecordNamedTuple(NamedTuple):
        shop_id: int
        delivery_days: int
        delivery_price: int


    class AltDict(NamedTuple):
        city: str
        tariffs: Tuple

    many_namedtuples3 = []
    for i in range(1000):
        many_namedtuples3.append(AltDict(
            city='0c5b2444-70a0-4932-980c-b4dc0d3f02b5',
            tariffs=(
                RecordNamedTuple(
                    shop_id=random.randint(1, 10000),
                    delivery_days=random.randint(1, 12),
                    delivery_price=random.randint(125, 888)
                ) for _ in range(3)
            ))
        )
    print(f'List[namedtuple3], mamory size: '
          f'{humanize_bytes(asizeof.asizeof(many_namedtuples3))}')


def main():
    list_of_dicts()
    list_of_dataclass()
    list_of_namedtuple()
    list_of_namedtuple_inheritance()
    best_case()


if __name__ == '__main__':
    main()
