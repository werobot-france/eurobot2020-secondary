import asyncio
import time
async def main():
  await asyncio.sleep(1)
  print('hello')
  print('world')

loop = asyncio.new_event_loop()
future = asyncio.create_task(main())
