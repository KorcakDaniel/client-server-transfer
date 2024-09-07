## Client-Server App

The task is to implement a simple client-server application using Python. The server listens for incoming connection from a client. Client attempts to connect to the server and establish a file transmission. The server receives transmitted file and saves it to a designated directory.


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
