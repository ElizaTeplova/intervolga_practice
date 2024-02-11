Получение данных о пользователях с помощью Log API Яндекс Метрики
===
## Зависимости & Настройка & Запуск
- Необходимо создать .env на том же уровне, что и .env.example. После этого вставить переменные из .env.example и присвоить им реальные значения. **(Изменено)**: Добавил в репозиторий заполненный .env
- Composer использует [PSR-4: Autoloader](https://www.php-fig.org/psr/psr-4/) и [phpdotenv](https://github.com/vlucas/phpdotenv)
- Необходимо запустить `composer install` в командной строке для загрузки зависимостей.
- Запускать код можно из командной строки `composer run-script intervolga` на уровне composer.json
- Полученный выходной файл должен быть на уровне cli.php в формате "log_counter_{$counterId}\_request_{$requestId}_all.csv"

## Структура проекта
```
C:.
│   .env.example
│   cli.php
│   composer.json
│
└───src
    └───App
        ├───Config
        │       RequestParams.php
        │
        ├───Exceptions
        │       HttpException.php
        │
        └───Services
                LogAPIService.php
```
## Работа кода
### RequestParams
---
Данный класс предназначен для инициализации параметров, по которым мы хотим получить данные. 
1. Указывается временной промежуток (по умолчанию год) 
```
$this->date1 = $date1 ?: date('Y-m-d', strtotime('-1 year'));
$this->date2 = $date2 ?: date('Y-m-d', strtotime('yesterday'));
```
2. Указывается источник логов. Допустимые значения: hits — просмотры, visits — визиты. (По умолчания визиты)
```
string $source = "visits"
```
3. Указваются поля о пользователях, которые мы хотим извлечь. В RequestParams.php подписаны все назначения полей. Подробнее: [просмотры](https://yandex.ru/dev/metrika/doc/api2/logs/fields/hits.html), [визиты](https://yandex.ru/dev/metrika/doc/api2/logs/fields/visits.html)

### LogAPIService
---
Для использование методов LogAPIService необходимо знать следующие параметры:
- COUNTER_ID - номер счетчика. Можно посмотреть [здесь](https://metrika.yandex.ru/list/)
- TOKEN - Авторизационный токен. [Подробнее](https://yandex.ru/dev/metrika/doc/api2/intro/authorization.html)

Класс предоставляет следующие возможности использования Log API Метрики

1. Оценка возможности получения данных при заданных параметрах. [Подробнее](https://yandex.ru/dev/metrika/doc/api2/logs/queries/evaluate.html)
  ```
  public function evaluateRequest(string $counterId, string $token, array $params): bool
  ```
2. Создание log-файла на стороне Яндекс Метрки с заданными параметрами. Возвращает номер запроса (request_id), по которому дальше можно будет узнать, на сколько файлов разбиты наши логи. [Подробнее](https://yandex.ru/dev/metrika/doc/api2/logs/queries/createlogrequest.html)
```
public function createLogs(string $counterId, string $token, array $params): string
```
3. Получение количества частей, на которые разбит log-файл (Исполнение до 2 минут). Метод ждет формирования файла на стороне Метрики и в случае успеха возвращает количество частей, на которые разбит наш log-файл. [Подробнее](https://yandex.ru/dev/metrika/doc/api2/logs/queries/getlogrequest.html)
```
public function getPartNumbers(string $counterId, string $token, string $requestId): int
```
4. Скачивание всех частей в один csv-файл. В случае успеха возвращает название полученного файла. [Подробнее](https://yandex.ru/dev/metrika/doc/api2/logs/queries/download.html)
```
public function downloadParts(string $counterId, string $token, string $requestId, int $partNums): string
```

5. Удаление log-файлов на стороне Яндекс Метрики. Т.к сформированные данные можно получить повторно уже из сформированного запроса (request_id), то чтобы отчистить данные, необходимо отдельно выполнить запрос. [Подробнее](https://yandex.ru/dev/metrika/doc/api2/logs/queries/clean.html)
```
public function cleanLogfile(string $counterId, string $token, string $requestId)
```

6. Исполнение предыдущих 5 шагов в одном методе. Необходимо указать номер счетчика, авторизационный токен, какие поля о пользователе мы хотим получить и нужно ли чистить логи на стороне метрики после получения csv-файла. Все шаги описаны [здесь](https://yandex.ru/dev/metrika/doc/api2/logs/practice/quick-start.html)
```
public function getCsvData(string $counterId, string $token, array $params, bool $cleanLog = true)
```
## References
- [Log API](https://yandex.ru/dev/metrika/doc/api2/logs/intro.html)


  
