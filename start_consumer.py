from consumer.consumer import start_consumer
import threading

if __name__ == '__main__':
    threading.Thread(target=start_consumer).start()
