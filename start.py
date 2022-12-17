from dotenv import load_dotenv

# Подгрузка окружения
load_dotenv()

from aiogram.utils import executor
from bot import dp


if __name__ == "__main__":
    executor.start_polling(dp)
