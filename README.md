# Сервис проведения тендеров

## Запуск сервиса в Docker
```docker-compose up -d``` - Работает по адресу localhost: 8080

## Маршруты (сервер ```/api```)
GET ```/ping``` - проверка работоспособности сервиса\
POST ```/tenders/new``` - создание нового тендера\
GET ```/tenders``` - получение списка тендеров\
GET ```/tenders/my``` - получение списка тендеров пользователя\
PATCH ```/tenders/{tenderId}/edit``` - изменение данных о тендере\
GET ```/tenders/{tenderId}/status``` - получение статуса тендера\
POST ```/bids/new``` - создание предложения по тендеру\
GET ```/bids/my``` - получение предложений пользователя\
GET ```/bids/{tenderId}/list``` - получения списка предложений для тендера\
GET ```/bids/{bidId}/status``` - получение статуса предложения\
PATCH ```/bids/{bidId}/edit``` - изменения данных о предложении\
PUT ```/bids/{bidId}/submit_decision``` - добавление решения по предложению\
PUT ```/bids/{bidId}/feedback``` - добавление комментария по предложению\

### Добавил файл .env-non-dev, для взаимодействия с БД в контейнере

## Стек
ЯП: Python\
Фрэймворки: FastAPI, SQLAlchemy, Pydantic\
БД: PostgreSQL\
а также Docker, Postman

## Структура проекта
```
src
  routing (контроллеры)
  schemas (модели БД, Pydantic)
  repositories (репозитории)
  config.py
  main.py
.env-non-dev
Dockerfile
docker-compose.yml
```
