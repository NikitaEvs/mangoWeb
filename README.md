# Mango
*A new time-management tool*

![unit_test](https://github.com/NikitaEvs/mangoWeb/workflows/unit_test/badge.svg)
![docker-deploy](https://github.com/NikitaEvs/mangoWeb/workflows/docker-deploy/badge.svg)
[![Coverage Status](https://coveralls.io/repos/github/NikitaEvs/mangoWeb/badge.svg?branch=tests&t=AYTufv)](https://coveralls.io/github/NikitaEvs/mangoWeb?branch=tests)
---
[Demo](http://51.15.97.72:8000/)

![](.github/pictures/mainPage.png)

![](.github/pictures/dayTask.png)

## Что это?
Большинство людей слушают музыку, механика её прослушивания всем понятна.
Выполнение задач чем-то похоже на прослушивание музыки, только "плейлист" создаётся
не на основе любимых песен, а на основе самых приоритетных задач.

__Mango__ - планировщик задач, который реализует эту концепцию.

Каждая задача представляет собой отдельный "трек", который можно включить, поставить
на паузу и выключить, текущая "композиция" находится в нижнем навбаре.

Можно добавлять, смотреть текущие задачи, смотреть задачи по дням, а также
все существующие задачи.

Для каждой задачи фиксируется время начала и время окончания (без учёта времени на паузе),
так что возможно оценить, сколько времени вы тратите на рутинные задачи *или же доверить
это дело ML (не реализовано)*, чтобы в будущем планировать время точно и оптимально.

## Техническая сторона
### Хочу посмотреть/собрать
#### Очень быстрый способ :rocket:
Зайти и посмотреть [сюда](http://51.15.97.72:8000/)
#### Но я хочу запустить на своей локальной машине :whale2:
Что же, вот [здесь](https://hub.docker.com/r/nikitaevs/mango) лежит
последняя стабильная сборка, прошедшая тесты. Как запустить?

Требования:

- [Docker](https://docs.docker.com/get-docker/)
- [Docker compose](https://docs.docker.com/compose/install/)

Для начала нужно склонить ветку с конфигурацией ```docker-compose.yml```
(она обновляется автоматичеcки)

```shell script
git clone --single-branch --branch docker https://github.com/NikitaEvs/mangoWeb.git
```

И поднять ```Docker```

```shell script
docker pull nikitaevs/mango
cd mangoWeb
docker-compose up -d
```

Готово!

Сервис работает на localhost:8000

#### Но я очень хочу собрать руками!

Что же, в таком случае обратитесь ко мне, я вышлю инструкцию ~~(зачем вам это)~~

### Немного про используемые технологии ~~(и инновации)~~
- Django
- PostgreSQL
- Bootstrap
- Docker
- GiHub Actions
- Coveralls

### Тесты
[![Coverage Status](https://coveralls.io/repos/github/NikitaEvs/mangoWeb/badge.svg?branch=tests&t=AYTufv)](https://coveralls.io/github/NikitaEvs/mangoWeb?branch=tests)

Написаны:

- [Unit тесты](tests/test_unit.py)
- [Тесты на views](tests/test_views.py)
- [Тесты на models](tests/test_model.py)
 
### CI/CD

- Для ```push``` и ```pull_request``` настроен
action, который прогоняет все тесты и
загружает отчёт на Coveralls

- Для ```pull_request``` в ```master``` и ```dev```
настроена сборка в ```Docker``` контейнер и загрузка на ```docker-hub``` 

### Известные проблемы

- Нельзя добавить задачи с одинаковым именем, если они обе активны

- При добавлении новой задачи, если такая уже существует, необходимо сначала
закрыть сообщение об ошибке, а только потом переходить на другую страницу

- В мобильной версии немного лагает parallax на главном экране