# ecomet_test
##Создание клауд функции
1) Код функции находится в /parser. Нужно задать переменные окружения, создав файл .env (как в .env.example)
2) Для депоя создал скрипт deploy_func.sh. Для создания архива функции нужно установить zip: 
```bash
    sudo apt install zip
```
3) Задать SERVICE_ACCOUNT_ID внутри скрипта (нужно для создания триггера)
4) Убедиться, что yandex cli установлен и настроен (https://yandex.cloud/ru/docs/cli/quickstart)
5) Запустить
```bash
    bash deploy_func.sh
```
## Запуск апи:
1) Создать файл .env и задать нужные настройки в нем (можно скопировать из .env.example дефолтные настройки)
2) ```bash
   docker-compose up --build
   ```
3) Таблицы не создаются, как было написано в задании
4) Доки находятся на /docs и /openapi.json
