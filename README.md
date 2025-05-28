# Приложение Погоды

## Описание

Это веб-приложение на базе Django, позволяющее пользователям искать прогнозы погоды по городам.

## Функции

*   **Прогноз погоды:** Пользователи могут ввести название города и просмотреть прогноз погоды для этого города с помощью API Open-Meteo.
*   **User Authentication:**  Возможности регистрации и входа пользователей.
*   **История поисков:** Сохраняет историю поиска для каждого пользователя.
*   **Контейнеризация:** Приложение контейнеризовано с использованием Docker для простоты развертывания.
*   **API статистики поиска:** Предоставляет конечную точку API для просмотра частоты поиска по городам.

## Используемые технологии

*   **Django:** Веб-фреймворк.
*   **Open-Meteo API:** Данные о погоде.
*   **Docker:** Контейнеризация.
*   **SQLite:** БД для хранения данных.

## Инструкция по запуску приложения

1.  **Склонируйте репозиторий:**

    ```bash
    git clone https://github.com/mrMaks2/test_task_O-complex.git
    cd weather_project
    ```

2.  **Создайте образ Docker:**

    ```bash
    docker build -t weather_app .
    ```

3.  **Запустите Docker-контейнер:**

    ```bash
    docker run -p 8000:8000 weather_app
    ```

4.  **Доступ к приложению:**

    Откройте веб-браузер и перейдите на страницу `http://localhost:8000/weather/`.

## Развертывание

1.  **Создайте виртуальную среду:**

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Linux/macOS
    venv\Scripts\activate  # On Windows
    ```

2.  **Установить зависимости:**

    ```bash
    pip install -r requirements.txt
    ```

3.  **Создайте миграции:**

    ```bash
    python manage.py makemigrations
    ```


4.  **Примите миграции:**

    ```bash
    python manage.py migrate
    ```

5.  **Создайте суперюзера:**

    ```bash
    python manage.py createsuperuser
    ```

6.  **Запустите сервер разработки:**

    ```bash
    python manage.py runserver
    ```

## Тесты

Для запуска тестов используйте следующую команду:

    python manage.py test weather_app