## Client-Server App

The task is to implement a simple client-server application using Python. The server listens for incoming connection from a client. Client attempts to connect to the server and establish a file transmission. The server receives transmitted file and saves it to a designated directory.

### Instructions
1. Create a virtual environment `python3 -m venv env`
2. Run the environment `source env/bin/activate`
3. Install the dependencies `pip install -r requirements.txt`
4. Run the server `python3 server.py` then the client `python3 client.py` retrospectively
5. Follow the instructions on screen


### Project Structure
- `README.md`: An overview and instructions.
- `server.py`: The Server implementation.
- `client.py`: The Client implementation.


### Server

- configurable
- after start-up it waits for a client connection
- after client connection is accepted, it receives a file from the client and saves it into designated directory
- if received file in the directory already exists, it is not overwritten


### Client

- configurable
- accepts input file with a path to file to be transmitted
- displays progress during the file transmission
