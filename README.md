## Описание приложения

Тестовое задание

Необходимо создать форму для отображения точек на карте используя некоторые сопутствующие хитрости


---
## Порядок развёртывания

### 1. Клонируем репозиторий (команда может отличаться в зависимости от пользователя!)
`git clone https://github.com/Wafflya/geotesttask.git`

### 2. Переходим в папку проекта
`cd geotesttask`

### 3. Копируем файл config.dist.ini в config.ini
`cp config.dist.ini config.ini`

### 4. Вписываем в config.ini валидные данные

### 5. Создаём виртаульное окружение 
`python3.9 -m venv env`

### 6. Активируем
`source env/bin/activate` (Linux)

### 7. Устанавливаем зависимости
 `pip3.9 install -r requirements.txt`
 
### 8. Запуск локального сервера (подходит только для тестирования):
 `python3.9 app.py`

### 9. Переходим по указанному УРЛ и наслаждаемся!