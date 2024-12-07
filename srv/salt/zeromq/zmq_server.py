import zmq
import threading
import logging
import time

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def server(port):
    context = zmq.Context()
    socket = context.socket(zmq.REP)
    socket.bind(f"tcp://*:{port}")
    
    while True:
        try:
            message = socket.recv_string()
            logger.info(f"Received request: {message}")
            # Simulate some processing time
            time.sleep(0.01)  # Adjust this to simulate more load or less
            socket.send_string(f"Processed: {message}")
        except zmq.ZMQError as e:
            logger.error(f"ZMQ Error: {e}")
            break

if __name__ == "__main__":
    server_thread = threading.Thread(target=server, args=(5555,))
    server_thread.start()
    
    # Keep the script running to prevent immediate exit
    while True:
        time.sleep(1)
