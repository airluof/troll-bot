import asyncio
from troll_bot.main import main

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    
    if loop.is_running():
        # Если цикл уже запущен, создаем задачу для main
        loop.create_task(main())
    else:
        try:
            asyncio.run(main())
        except Exception as e:
            print(f"An error occurred: {e}")
