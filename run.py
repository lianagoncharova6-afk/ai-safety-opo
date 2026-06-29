"""
Скрипт запуска приложения.
Выполняет создание таблиц БД и запускает uvicorn-сервер.
"""
import uvicorn
from app.database import engine, Base

def init_db():
    """Создать все таблицы в БД."""
    print("Инициализация базы данных...")
    Base.metadata.create_all(bind=engine)
    print("Таблицы созданы успешно.")

if __name__ == "__main__":
    init_db()
    print("Запуск сервера: http://127.0.0.1:8000")
    uvicorn.run(
        "app.main:app",
        host="127.0.0.1",
        port=8000,
        reload=True,
    )
