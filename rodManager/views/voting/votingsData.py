from datetime import datetime
from typing import List, Optional


class Option:
    def __init__(self, option_id: int, label: str, votes: int):
        self.optionId = option_id
        self.label = label
        self.votes = votes


class VotingTopic:
    def __init__(self, _id: int, title: str, description: str, options: List[Option], finish_date: Optional[datetime]):
        self.id = _id
        self.title = title
        self.description = description
        self.options = options
        self.finishDate = finish_date


# Konwersja danych

def convert_to_datetime(date_str: str) -> datetime:
    return datetime.fromisoformat(date_str)


converted_votings = [
    VotingTopic(
        _id=1,
        title='Temat 1',
        description='Opis tematu 1',
        options=[
            Option(option_id=1, label='Opcja 1', votes=0),
            Option(option_id=2, label='Opcja 2', votes=0),
            Option(option_id=3, label='Opcja 3', votes=0)
        ],
        finish_date=convert_to_datetime("2024-10-10T12:00:00")
    ),
    VotingTopic(
        _id=2,
        title='Temat 2',
        description='Opis tematu 2',
        options=[
            Option(option_id=1, label='Opcja 1', votes=0),
            Option(option_id=2, label='Opcja 2', votes=0),
            Option(option_id=3, label='Opcja 3', votes=0)
        ],
        finish_date=convert_to_datetime("2024-10-20T12:00:00")
    ),
    VotingTopic(
        _id=3,
        title='Opinia na temat nowych zasad ogrodów działkowych',
        description='Prosimy o opinię na temat proponowanych zmian w regulaminie ogródków działkowych',
        options=[
            Option(option_id=1, label='Zgadzam się z propozycjami', votes=235),
            Option(option_id=2, label='Nie mam zdania', votes=320),
            Option(option_id=3, label='Nie zgadzam się z propozycjami', votes=120),
            Option(option_id=4, label='Wstrzymuję się od głosu', votes=120),
        ],
        finish_date=convert_to_datetime("2023-10-10T12:00:00")
    ),
    VotingTopic(
        _id=4,
        title='Wybór nowego miejsca na plac zabaw dla dzieci',
        description='Prosimy o wybór najlepszego miejsca na nowy plac zabaw dla dzieci w obrębie ogrodu działkowego',
        options=[
            Option(option_id=1, label='Zielona Łąka', votes=450),
            Option(option_id=2, label='Sosnowy Gaj', votes=345),
            Option(option_id=3, label='Brzozowy Zakątek', votes=25),
        ],
        finish_date=convert_to_datetime("2023-10-20T12:00:00"),
    ),
    VotingTopic(
        _id=5,
        title='Wybór rośliny na nowy centralny klomb ogrodowy',
        description='Prosimy o wybór rośliny, która będzie głównym elementem w nowym centralnym kształcie klombu ogrodowego',
        options=[
            Option(option_id=1, label='Róża', votes=50),
            Option(option_id=2, label='Tulipan', votes=30),
            Option(option_id=3, label='Lawenda', votes=25),
            Option(option_id=4, label='Stokrotka', votes=40),
            Option(option_id=5, label='Irys', votes=15),
            Option(option_id=6, label='Narcyz', votes=20),
            Option(option_id=7, label='Begonia', votes=35),
            Option(option_id=8, label='Goździk', votes=22),
            Option(option_id=9, label='Peon', votes=28),
            Option(option_id=10, label='Fiołek', votes=18)
        ],
        finish_date=convert_to_datetime("2023-11-10T12:00:00")),
]

# Przykład użycia:
for topic in converted_votings:
    print(f"Title: {topic.title}")
print(f"Description: {topic.description}")
print("Options:")
for option in topic.options:
    print(f"- {option.label}: {option.votes} votes")
print(f"Finish Date: {topic.finishDate}")
print("-----------")
