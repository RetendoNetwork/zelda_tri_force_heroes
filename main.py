import threading
import grpc

# Simulate the nex module with start functions
class Nex:
    @staticmethod
    def start_authentication_server():
        print("Starting Authentication Server...")

    @staticmethod
    def start_secure_server():
        print("Starting Secure Server...")

nex = Nex()

def main():
    threads = []

    # Start Authentication Server
    auth_thread = threading.Thread(target=nex.start_authentication_server)
    threads.append(auth_thread)
    auth_thread.start()

    # Start Secure Server
    secure_thread = threading.Thread(target=nex.start_secure_server)
    threads.append(secure_thread)
    secure_thread.start()

    # Wait for all threads to complete
    for thread in threads:
        thread.join()

if __name__ == "__main__":
    main()
