FROM python:3.12-slim

# Устанавливаем системные зависимости
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Устанавливаем Poetry
RUN curl -sSL https://install.python-poetry.org | python3 - \
    && ln -s /root/.local/bin/poetry /usr/local/bin/poetry

WORKDIR /app

# Копируем файлы зависимостей
COPY pyproject.toml poetry.lock* ./

# ТОЛЬКО ЭТИ ДВЕ КОМАНДЫ - никаких experimental!
RUN poetry config virtualenvs.create false

# Экспортируем requirements и устанавливаем через pip
RUN pip install --upgrade pip \
    && pip install poetry-plugin-export \
    && poetry export -f requirements.txt --output requirements.txt --without-hashes \
    && pip install --no-cache-dir -r requirements.txt

# Копируем остальной код
COPY . .

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]