# Task Processing System

Микросервисная система обработки задач с использованием API, RabbitMQ, PostgreSQL, воркеров и Kubernetes с автомасштабированием.

---

## Описание

Этот проект реализует архитектуру, в которой задачи создаются через API, кладутся в очередь RabbitMQ, воркеры обрабатывают задачи и обновляют их статусы в базе данных PostgreSQL. Воркеры и API сервис запущены в Kubernetes, настроено автомасштабирование воркеров.

---

## Технологии

- Python 3.10+
- FastAPI
- SQLAlchemy (async)
- PostgreSQL
- RabbitMQ
- Docker, Docker Compose
- Kubernetes + HPA (Horizontal Pod Autoscaler)
- aio-pika для работы с RabbitMQ
- Logging, async/await

---

## Установка

1. Клонируйте репозиторий
2. Создайте файл .env на основе следующего:
<pre>
  DATABASE_URL= 
  RABBITMQ_URL= 
  RABBITMQ_QUEUE_NAME= 
  WORKER_TIMEOUT= 
  MAX_RETRIES= 
  PORT= 
  NODE_ENV= 
</pre>
3.Запустите сервисы:
    docker-compose up --build
4.API будет доступен по адресу: http://localhost:3000
5.RabbitMQ Management UI: http://localhost:15672 (логин/пароль из .env)

## Запуск в Kubernetes

Убедитесь, что у вас есть доступ к Kubernetes (например, minikube или кластер в облаке).

Примените манифесты:

    kubectl apply -f k8s/

Проверьте статус подов и автомасштабирования:

    kubectl get pods
    kubectl get hpa

## API эндпоинты

    POST /api/tasks — Создание новой задачи
    Тело запроса:

    {
      "title": "Название задачи",
      "description": "Описание",
      "priority": "high|medium|low"
    }

    GET /api/tasks/{id} — Получить статус задачи

    GET /api/tasks — Получить список задач с пагинацией

    GET /health — Проверка состояния сервиса

## Особенности

    Асинхронная обработка задач через RabbitMQ и воркеры
    Использование SQLAlchemy с async для работы с PostgreSQL
    Автомасштабирование воркеров в Kubernetes на основе CPU и длины очереди RabbitMQ
    Логирование и graceful shutdown воркеров



