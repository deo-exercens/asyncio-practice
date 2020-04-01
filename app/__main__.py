import asyncio
import functools
import signal
from datetime import datetime

from app import logger
from app.core import all_task_exit, consume, publish
from app.models import Message


def main():
    queue = asyncio.Queue()
    loop = asyncio.get_event_loop()
    __init_handler(loop)

    try:
        for i in range(5):
            message = Message(seqno=i, contents='test', dt=datetime.now())
            loop.create_task(publish(queue=queue, message=message))
        loop.create_task(consume(queue=queue))
        loop.run_forever()
    except KeyboardInterrupt:
        logger.info("exit")
    finally:
        loop.close()


def __init_handler(loop):
    '''
    add signal handler for exit
    add global exception handler
    '''
    exit_signals = (signal.SIGHUP, signal.SIGTERM, signal.SIGINT)
    for signal_ in exit_signals:
        loop.add_signal_handler(
            signal_,
            lambda signal_=signal_: asyncio.create_task(all_task_exit(loop=loop, signal=signal_)))
    loop.set_exception_handler(__handle_exception)


def __handle_exception(loop, context):
    msg = context.get("exception", context["message"])
    logger.error(f"Caught exception: {msg}")
    asyncio.create_task(all_task_exit(loop))


if __name__ == "__main__":
    main()
