import hashlib
import logging
import os
import socket
import time
from pathlib import Path

from tqdm import tqdm

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter("[%(name)s] %(asctime)s %(levelname)s - %(message)s")
handler = logging.StreamHandler()
logger.addHandler(handler)


IP_ADDRESS = "127.0.0.1"
PORT = 3254
SERVER_DIR = "server"
CHUNK_BYTES = 1024


def is_file(file_path: str) -> bool:
    """Check if a file exists"""
    if os.path.exists(file_path):
        return True
    return False


def get_size(file_path: str) -> int:
    return os.path.getsize(file_path)


def create_directory() -> None:
    """Create a server directory, if it doesn't exist"""
    if not os.path.isdir(SERVER_DIR):
        os.makedirs(SERVER_DIR)
        logger.info(f'A directory "{SERVER_DIR}" was created')


def alter_file_path(file_path: str) -> str:
    """Alter the file path to include the server designated folder"""
    return os.path.join(SERVER_DIR, Path(file_path).name)


def compute_file_hash(file_path: str, hash_algo="sha256") -> str:
    """Compute hash of the file using the specified algorithm (default: SHA-256)."""
    hash_func = hashlib.new(hash_algo)
    with open(file_path, "rb") as file:
        while chunk := file.read(4096):
            hash_func.update(chunk)
    return hash_func.hexdigest()


def verify_hash(file_path: str, hash: str) -> bool:
    """Compares the original hash with the hash of a file"""
    computed_hash = compute_file_hash(file_path)
    logger.debug(f"Desired hash: {hash}\nComputed hash: {computed_hash}")
    return computed_hash == hash


def receive_file(client_socket: socket.socket) -> None:
    """Receive a file from the client"""
    details = client_socket.recv(CHUNK_BYTES).decode().split("|")

    client_file_path = details[0]
    client_file_size = int(details[1])
    client_file_hash = details[2]

    server_file_path = alter_file_path(client_file_path)

    # TODO: Metadata comparison, send response back to the client
    if (
        is_file(server_file_path)
        and get_size(server_file_path)
        and verify_hash(server_file_path, client_file_hash)
    ):
        logger.warning("Identical file already exists")
        return None

    with open(server_file_path, "wb") as file:
        with tqdm(
            total=client_file_size,
            unit="B",
            unit_scale=True,
            desc="Receiving file...",
        ) as progress:
            total_sent = 0
            while total_sent <= client_file_size:
                data = client_socket.recv(CHUNK_BYTES)
                if not (data):
                    break
                file.write(data)
                total_sent += len(data)
                progress.update(len(data))

        if total_sent == client_file_size:
            logger.info("File transferred successfully!")
        else:
            logger.error("Something went wrong with the file transfer")


def main():
    create_directory()
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((IP_ADDRESS, PORT))
    logger.info("Waiting for a connection...")
    s.listen(0)
    while True:
        client_socket, client_address = s.accept()
        logger.info(f"{client_address} connected to the server")
        receive_file(client_socket)
        client_socket.close()


if __name__ == "__main__":
    main()
