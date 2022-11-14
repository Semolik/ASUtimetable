# Altai State University timetable
Веб приложение для просмотра расписания Алтайского государственного университета.
## Установка
### frontend
    cd client
    npm install
### backend
    docker-compose build
## Настройка
Для запуска локально поменять в файле [http-common.vue](src/http-common.vue) переменую на ссылку в локальной сети
    
    baseURL: '/api',

## Запуск
### frontend
    cd client
    npm run dev
### backend
    docker-compose up
