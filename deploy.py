import docker
import time

def create_uptime_kuma():
    # 1. Подключаемся к Docker-демону (использует стандартный сокет)
    client = docker.from_env()

    print("Проверяем наличие образа Uptime Kuma...")
    # Опционально: можно заранее скачать образ, чтобы контейнер запустился быстрее
    # client.images.pull('louislam/uptime-kuma:2')

    print("Создаем и запускаем контейнер...")
    try:
        # 2. Запускаем контейнер. Это аналог команды docker run
        container = client.containers.run(
            image='louislam/uptime-kuma:2',
            name='uptime-kuma-auto',        # Имя контейнера
            detach=True,                    # Запуск в фоновом режиме
            restart_policy={"Name": "unless-stopped"}, # Автоперезапуск
            ports={'3001/tcp': 3001},       # Проброс порта: хост:контейнер
            volumes={
                # Важный момент: persistent volume, чтобы данные не терялись при пересоздании
                'uptime-kuma-data': {'bind': '/app/data', 'mode': 'rw'}
            }
        )
        print(f"✅ Контейнер успешно запущен! ID: {container.short_id}")
        print(f"🌐 Uptime Kuma доступна по адресу: http://localhost:3001")
        
        # Даем контейнеру пару секунд, чтобы он точно поднялся
        time.sleep(2)
        container.reload()
        print(f"📊 Текущий статус: {container.status}")

    except docker.errors.APIError as e:
        print(f"❌ Ошибка при запуске контейнера: {e}")

if __name__ == "__main__":
    create_uptime_kuma()
