# Altai State University timetable
Сайт АГУ обновили, теперь парсер не актуален.

Веб приложение для просмотра расписания Алтайского государственного университета.
## Установка
### frontend
    cd client
    npm install
### backend
    docker-compose build
## Настройка
Для запуска локально поменять в файле [http-common.vue](client/src/http-common.vue) переменую на ссылку в локальной сети
    
    baseURL: '/api',

## Запуск
### frontend
    cd client
    npm run dev
### backend
    docker-compose up
## Скриншоты
### Главная страница
На главной странице отображаются избранные группы

![image](https://user-images.githubusercontent.com/70706334/201716188-3e0a52aa-e7e3-4566-a4e6-7b401da3ad89.png)
### Страница группы
![image](https://user-images.githubusercontent.com/70706334/201716372-4fdae0a0-7ff1-455f-9715-535dd697234a.png)
### Выбор факультета
![image](https://user-images.githubusercontent.com/70706334/201716990-39a54a7c-6922-4685-af6c-a79204cf0b52.png)
### Выбор группы
![image](https://user-images.githubusercontent.com/70706334/201717257-ef92b741-d75a-4452-902c-eb6417ec1778.png)
