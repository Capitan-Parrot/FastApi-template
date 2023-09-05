
<div align="center">
  <h3 align="center">Шаблон FastApi для МВП</h3>

  <p align="center">
    Структура проекта для легкой разработки 
  </p>
</div>


### О чём проект
Минималистичный шаблон с удобной структурой проекта для использования в петпроектах или при создания MVP на хакатонах

### Используемые технологии

[//]: # (![GitLab CI]&#40;https://img.shields.io/badge/gitlab%20ci-%23181717.svg?style=for-the-badge&logo=gitlab&logoColor=white&#41;)
![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)
![Postgres](https://img.shields.io/badge/postgres-%23316192.svg?style=for-the-badge&logo=postgresql&logoColor=white)
![Redis](https://img.shields.io/badge/redis-%23DD0031.svg?style=for-the-badge&logo=redis&logoColor=white)
![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white)
![Prometheus](https://img.shields.io/badge/Prometheus-E6522C?style=for-the-badge&logo=Prometheus&logoColor=white)
![Heroku](https://img.shields.io/badge/heroku-%23430098.svg?style=for-the-badge&logo=heroku&logoColor=white)

### Работа с сервисом

Сервис доступен по ссылке:  [https://test-fastapi-template-3880ff94f1d6.herokuapp.com/](https://test-fastapi-template-3880ff94f1d6.herokuapp.com/)
Вы можете использовать его для тестирования. Однако, если вы хотите запустить сервис локально, то вам необходимо выполнить следующие действия:

### Локальный запуск

Перед тем, как развернуть у себя сервис необходимо установить [Docker](https://docs.docker.com/get-docker/) и [Docker Compose](https://docs.docker.com/compose/install) на вашу машину.

Далее, необходимо выполнить следующие действия:

```bash
# Клонируем репозиторий
git clone -b master https://github.com/Capitan-Parrot/FastApi-template.git
# Переходим в папку с проектом
cd FastApi-template
# Запускаем сервис
docker-compose up -d --build
```

Теперь вы можете открыть в браузере [localhost](http://localhost:8000) и увидеть работающий сервис.
