# Сайт разработан мною для компании "ELECTRO-ENGINEERING" при помощи фреймворка Django

<p align="center">
  <a href="http://18.212.252.188"><img src="https://github.com/yarstein/eleng/blob/main/Logo.png" alt='Eleng'></a>
</p>

---
## Описание

Этот проект представляет собой веб-сайт, разработанный с использованием фреймворка Django. Компания специализируется на разработке электрооборудования и предоставляет каталог продукции и услуг. Цены на изделия устанавливаются менеджерами и не отображаются на сайте. Чтобы узнать цену или получить подробную информацию о изделиях, пользователи должны авторизоваться (требуется подтвержения почты), добавить изделие в корзину, оставить комментарий в заказе, оформить заказ. Менеджеры обрабатывают запросы через админ-панель, а ответы отправляются на электронную почту.

<p align="center">
  <img src="https://github.com/yarstein/eleng/blob/main/zakaz.png" alt='Zakaz'></a>
</p>

Сайт включает раздел "Каталог" с товарами и услугами, где пользователи могут оставлять комментарии под каждым изделием. Главная страница содержит слайдер, информацию об услугах, управляемых через админ-панель, и ленту новостей. Также на сайте размещена информация о компании, контактные данные, возможность отправлять резюме и просматривать вакансии. Для неавторизованных пользователей включена функция CAPTCHA при отправке данных при помощи форм.

## Основные функции
* **Авторизация пользователей**
* **Профиль пользователя**
* **Главная страница со слайдером, услугами и новостями**
* **Управление заказами через админ-панель**
* **Отправка уведомлений по электронной почте**
* **Раздел "Каталог" с детальным описанием товаров и возможностью оставлять комментарии**
* **Раздел "О компании" с контактной информацией**
* **Раздел "Карьера" информация о вакансиях и отправка резюме**

## Используемые технологии
- **Языки программирования**: Python
- **Фреймворки**: Django
- **Базы данных**: PostgreSQL
- **Кэширование**: Redis
- **Асинхронные задачи**: Celery
- **Фронтенд**: HTML, CSS, JavaScript (Django templates)
- **Аутентификация**: Google OAuth2
- **Электронная почта**: SMTP

## Сторонние библиотеки
- `mptt`: Библиотека для работы с древовидными структурами данных. Реализована иерархическая структура категорий товаров, а также система древовидной комментарий. Также используется в админ-панели.
- `ckeditor`: WYSIWYG редактор, который позволяет администраторам редактировать текстовый контент на сайте.
- `ckeditor_uploader`: Расширение для CKEditor, которое добавляет возможность загрузки и управления файлами и изображениями.
- `social_django`: Пакет для интеграции социальной аутентификации в Django, используется для Google.
- `django_extensions`: Набор полезных расширений и утилит для разработки на Django, включая команды для управления проектом и дополнительные поля моделей.
- `captcha`: Django-приложение для добавления капчи (CAPTCHA) на формы, для защиты от лишнего спама.
- `debug_toolbar`: Панель инструментов для отладки, которая предоставляет детальную информацию о запросах, SQL-запросах, шаблонах и многом другом, что упрощает отладку и оптимизацию кода.
## Установка и запуск проекта

### Предварительные требования

Убедитесь, что у вас установлены следующие программы:

- Python 3.x
- PostgreSQL
- Redis
- Git

### Шаги установки

1. Клонируйте репозиторий:

    ```sh
    git clone https://github.com/yarstein/eleng.git
    cd eleng
    ```

2. Создайте и активируйте виртуальное окружение:

    ```sh
    python -m venv venv
    source venv/bin/activate  # Для Windows: venv\Scripts\activate
    ```

3. Установите зависимости:

    ```sh
    pip install -r requirements.txt
    ```

4. Создайте файл `.env` в корне проекта и добавьте туда конфиденциальные данные:

    ```plaintext
    SECRET_KEY=your_secret_key
    DEBUG=True
    DB_NAME=your_db_name
    DB_USER=your_db_user
    DB_PASSWORD=your_db_password
    SOCIAL_AUTH_GOOGLE_OAUTH2_KEY=your_google_oauth2_key
    SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET=your_google_oauth2_secret
    EMAIL_HOST_USER=your_email_host_user
    EMAIL_HOST_PASSWORD=your_email_host_password
    ```

5. Примените миграции базы данных:

    ```sh
    python manage.py migrate
    ```

6. Соберите статические файлы:

    ```sh
    python manage.py collectstatic
    ```

7. Запустите сервер Redis:
   
   ```sh
   sudo service redis-server start
   ```

8. Запустите Celery для отправки электронных писем:
   
   ```sh
   celery -app=eleng worker --loglevel=info --pool=solo
   ```

9.  Запустите сервер разработки:

    ```sh
    python manage.py runserver
    ```
## Лицензия

В настоящее время у проекта нет лицензии.

## Контакты

- Telegram: [@yarstein](https://t.me/yarstein)
