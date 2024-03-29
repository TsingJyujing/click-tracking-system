import time
from queue import Queue
from threading import Lock, Thread

from click_ts.settings import DEBUG
from config import QUEUE_MAX_SIZE, QUEUE_WRITING_LIMIT, QUEUE_WAITING_TIME, get_logging_collection, \
    get_logging_connection

logging_queue = Queue(maxsize=QUEUE_MAX_SIZE)

operation_lock = Lock()

conn = get_logging_connection()


def queue_provide(data):
    """
    Insert a data into queue
    :param data:
    :return:
    """
    logging_queue.put(data)
    if logging_queue.qsize() > QUEUE_WRITING_LIMIT:
        clean_buffer()


def clean_buffer():
    """
    Clear all the data in the queue
    :return:
    """
    if not logging_queue.empty():
        try:
            operation_lock.acquire()
            logs = []
            while not logging_queue.empty() and len(logs) < QUEUE_MAX_SIZE:
                logs.append(logging_queue.get())
            if DEBUG:
                print("Queue cleaned, insert {} logs.".format(len(logs)))
            if len(logs) > 0:
                get_logging_collection(conn).insert_many(logs)
        finally:
            try:
                operation_lock.release()
            except RuntimeError as _:
                pass


class TimedCleanQueue(Thread):
    """
    This is the thread for monitoring the queue periodically
    If the size too large than clean it
    """

    def __init__(self, waiting_time: float):
        """
        :param waiting_time: Sleep time (in seconds) during 2 steps
        """
        super().__init__()
        self.is_stop = False
        self.waiting_time = waiting_time

    def run(self) -> None:
        print("Queue cleaning thread started.")
        while not self.is_stop:
            time.sleep(self.waiting_time)
            clean_buffer()


monitor_thread = TimedCleanQueue(QUEUE_WAITING_TIME)
monitor_thread.setDaemon(True)
monitor_thread.start()
