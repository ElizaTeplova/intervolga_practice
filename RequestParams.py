from dataclasses import dataclass, field
from datetime import date, timedelta


@dataclass
class RequestParams:
    start_date: str = date.today().replace(year=date.today().year - 1)
    end_date: str = date.today() - timedelta(days=1)
    fields: list[str] = field(default_factory=lambda: [
        'ym:s:visitID',  # Идентификатор визита
        'ym:s:clientID',  # Анонимный идентификатор пользователя в браузере (first-party cookies)
        'ym:s:date',  # Дата визита
        'ym:s:watchIDs',  # Просмотры, которые были в данном визите. Ограничение массива — 500 просмотров
        'ym:s:startURL',  # Страница входа
        'ym:s:endURL',  # Страница выхода
        'ym:s:pageViews',  # Глубина просмотра (детально)
        'ym:s:visitDuration',  # Время на сайте (детально)
        'ym:s:regionCountry',  # ID страны
        'ym:s:regionCity',  # ID города
        'ym:s:goalsID',  # Номера целей, достигнутых за данный визит
        'ym:s:goalsSerialNumber',  # Порядковые номера достижений цели с конкретным идентификатором
        'ym:s:referer',  # Реферер
        'ym:s:deviceCategory',
        # Тип устройства. Возможные значения: 1 — десктоп, 2 — мобильные телефоны, 3 — планшеты, 4 — TV
        'ym:s:operatingSystem',  # Операционная система (детально)
        'ym:s:browser',  # Браузер
    ])
    source: str = 'visits'