**Запуск проекта локально**

```bash
brew install uv
```

```bash
uv sync
uv build
```

```
Создайте файл .env и внесите в него свои данные
```
``` bash
uv run python -m uvicorn src.backend.main:app --reload  
```

**Запуск через docker**
```bash
docker-compose -f docker-compose.yml up --build -d
```

**Дока лежит по localhost/docs**

