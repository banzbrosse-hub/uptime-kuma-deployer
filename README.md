# Uptime Kuma Deployer

Python-скрипт для автоматического развертывания Uptime Kuma в Docker-контейнере с готовыми оповещениями в Telegram.

## Зачем это нужно?
Ручное развертывание Uptime Kuma с настройкой алертов занимает время. 
Этот скрипт делает все за одну команду.

## Что делает?
- Создает Docker-контейнер с Uptime Kuma
- Настраивает persistent volume (данные не теряются)
- Пробрасывает порт 3001
- Готов к подключению Telegram-бота

## Быстрый старт
```bash
# Клонируйте репозиторий
git clone https://github.com/banzbrosse-hub/uptime-kuma-deployer.git
cd uptime-kuma-deployer

# Установите зависимости
pip install -r requirements.txt

# Запустите
python deploy.py
