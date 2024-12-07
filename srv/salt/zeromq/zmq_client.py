import zmq
import threading
import logging
import random
import time

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def client(id, server_ip, server_port, num_requests=100):
    context = zmq.Context()
    socket = context.socket(zmq.REQ)
    socket.connect(f"tcp://{server_ip}:{server_port}")
    
    for i in range(num_requests):
        message = f"Client {id} - Request {i}"
        try:
            socket.send_string(message)
            response = socket.recv_string()
            logger.info(f"Client {id}: {response}")
            # Random sleep to simulate different timing in real scenarios
            time.sleep(random.uniform(0.01, 0.1))  # Adjust for more or less realistic load
        except zmq.ZMQError as e:
            logger.error(f"Client {id} ZMQ Error: {e}")

def run_clients(num_clients, server_ip="localhost", server_port=5555):
    threads = []
    for i in range(num_clients):
        thread = threading.Thread(target=client, args=(i, server_ip, server_port))
        threads.append(thread)
        thread.start()
    
    for thread in threads:
        thread.join()

if __name__ == "__main__":
    # Number of clients (minions) to simulate
    run_clients(100)  # Adjust this number to simulate more or fewer minions
