import hashlib
import logging
import os
import socket
import time
from typing import Optional

from tqdm import tqdm

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter("[%(name)s] %(asctime)s %(levelname)s - %(message)s")
handler = logging.StreamHandler()
logger.addHandler(handler)


PORT = 3254
CLIENT_DIR = "client"
CHUNK_BYTES = 1024


def check_directory() -> bool:
    """Check if the specified directory exists or not"""
    if not os.path.isdir(CLIENT_DIR):
        os.makedirs(CLIENT_DIR)
        logger.info(f'A directory "{CLIENT_DIR}" was created')
        logger.info(f'Please supply the file to the "{CLIENT_DIR}" directory')
        return False
    return True


def get_file() -> str:
    """Get file from user input"""
    while True:
        file_name = input("File to transfer: ")
        file_path = os.path.join(CLIENT_DIR, file_name)
        if os.path.exists(file_path):
            return file_path
        logger.error(f"{file_name} doesn't exist in the {CLIENT_DIR} directory")


def get_server() -> str:
    """Get the server address from user input"""
    return input("Server address: ")


def connect(server: str) -> Optional[socket.socket]:
    """Establish connection between server and client"""
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.connect((server, PORT))
        return s
    except socket.error as e:
        logger.info("Couldn't connect to a server...")
        logger.debug(e)
        return None


def compute_file_hash(file_path: str, hash_algo="sha256") -> str:
    """Compute hash of the file using the specified algorithm (default: SHA-256)."""
    hash_func = hashlib.new(hash_algo)
    with open(file_path, "rb") as file:
        while chunk := file.read(4096):
            hash_func.update(chunk)
    return hash_func.hexdigest()


def send_file(s: socket.socket, file_path: str) -> None:
    """Attempt to send a file to the server"""
    file_size = os.path.getsize(file_path)
    file_hash = compute_file_hash(file_path)
    total_sent = 0

    s.send(f"{file_path}|{file_size}|{file_hash}".encode("utf-8"))

    with open(file_path, "rb") as file:
        with tqdm(
            total=file_size, unit="B", unit_scale=True, desc="Sending file..."
        ) as progress:
            while data := file.read(CHUNK_BYTES):
                s.sendall(data)
                total_sent += len(data)
                progress.update(len(data))

    if total_sent == file_size:
        logger.info("File transferred successfully!")
    else:
        logger.error("Something went wrong with the file transfer")


def main():
    while not check_directory():
        time.sleep(10)

    sock = None
    server = get_server()
    while True:
        sock = connect(server)
        if sock:
            logger.info("Connected successfully!")
            break
        logger.info("Retrying in 2 seconds...")
        time.sleep(2)

    send_file(sock, get_file())
    sock.close()


if __name__ == "__main__":
    main()
