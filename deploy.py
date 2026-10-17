import os
import time
import docker
from dotenv import load_dotenv

# Загружаем переменные из .env (если файл есть)
load_dotenv()

CONTAINER_NAME = os.getenv("CONTAINER_NAME", "uptime-kuma-auto")
PORT = os.getenv("KUMA_PORT", "3001")


def deploy_kuma():
    print("🔄 Подключаемся к Docker...")
    try:
        client = docker.from_env()
    except docker.errors.DockerException:
        print("❌ Ошибка: Docker не запущен или не установлен на этом компьютере.")
        return

    # Проверяем, не запущен ли уже такой контейнер
    try:
        existing = client.containers.get(CONTAINER_NAME)
        print(f"⚠️ Контейнер '{CONTAINER_NAME}' уже существует (статус: {existing.status}).")
        print("Если хотите пересоздать его, удалите старый контейнер вручную.")
        return
    except docker.errors.NotFound:
        pass  # Контейнера нет, идем дальше

    print(f"🚀 Создаем и запускаем контейнер '{CONTAINER_NAME}'...")
    try:
        container = client.containers.run(
            image='louislam/uptime-kuma:2',
            name=CONTAINER_NAME,
            detach=True,
            restart_policy={"Name": "unless-stopped"},
            ports={'3001/tcp': int(PORT)},
            volumes={
                'uptime-kuma-data': {'bind': '/app/data', 'mode': 'rw'}
            }
        )
        print(f"✅ Успешно! ID контейнера: {container.short_id}")
        print(f"🌐 Uptime Kuma доступна по адресу: http://localhost:{PORT}")

        # Даем секунду на запуск и проверяем статус
        time.sleep(2)
        container.reload()
        print(f"📊 Текущий статус: {container.status}")

    except docker.errors.APIError as e:
        print(f"❌ Ошибка Docker API: {e}")
    except Exception as e:
        print(f"❌ Неизвестная ошибка: {e}")


if __name__ == "__main__":
    deploy_kuma()