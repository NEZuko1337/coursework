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

**Дока лежит по localhost/docs**

**Добавить докерфайл + компоуз + починить фронт**