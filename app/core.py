'''
core.py

async pub/sub
'''
import asyncio
import random
from typing import Any

from app import logger
from app.models import Message


async def publish(queue: asyncio.Queue, message: Any):
    ''' publish '''
    logger.info(message)
    await queue.put(message)


async def consume(queue: asyncio.Queue):
    ''' consume '''
    while True:
        try:
            message = await queue.get()
        except asyncio.CancelledError:
            break
        else:
            logger.info(message)

        # i/o bound work
        await asyncio.sleep(random.random())


async def all_task_exit(loop, signal=None):
    '''
    gracefully exit
    '''
    logger.info(f'signal: {signal}')
    tasks = [
        task
        for task in asyncio.all_tasks()
        if task is not asyncio.current_task()]
    logger.info(f'{len(tasks)} task exit: \n{tasks}')
    [task.cancel() for task in tasks]

    await asyncio.gather(*tasks, return_exceptions=True)
    loop.stop()
