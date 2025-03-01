## Дополнения к реализации проекта:
В рамках экономии времени были пропущены некоторые вещи:
- асинхронные запросы к БД
- написание тестов (работоспособность была проверена вручную, возникли проблемы с тестовыми фикстурами и подменой Dependencies)
- вынесение логики из роутера в сервисы
- также более сложной проверки требует работа с паролями (например передача этого функционала в Keycloak)
- отсутствует кэш
- alembic (для работы с базой и изменением моделей лучше использовать миграции)
- .gitignore и .dockerignore

Проект полностью проходит линтеры (isort, ruff, mypy - с парой игноров)

## Запуск проекта локально:
Переименуйте .env.example в .env
```
docker compose up -d --build
```

После этого по адресу:
localhost:8000/docs  
Будет доступна документация к запущенному проекту.

### DEBUG
В случае если в .env указано DEBUG=True,  
то будет создан staff пользователь.