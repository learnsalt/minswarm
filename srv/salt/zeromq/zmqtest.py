import zmq
import threading
import time

# Server part (simulating Salt Master)
def server():
    context = zmq.Context()
    socket = context.socket(zmq.REP)
    socket.bind("tcp://*:5555")  # Use appropriate port
    while True:
        # Wait for next request from client
        message = socket.recv()
        print(f"Received request: {message}")
        socket.send(b"World")

# Client part (simulating Salt Minions)
def client(id):
    context = zmq.Context()
    socket = context.socket(zmq.REQ)
    socket.connect("tcp://localhost:5555")
    for request in range(10):
        socket.send_string(f"Hello from client {id}")
        message = socket.recv()
        print(f"Client {id} received reply {message}")

if __name__ == "__main__":
    # Start server
    server_thread = threading.Thread(target=server)
    server_thread.start()

    # Start multiple clients
    clients = [threading.Thread(target=client, args=(i,)) for i in range(100)]  # Adjust number of clients
    for c in clients:
        c.start()

    time.sleep(30)  # Let clients run for 30 seconds
