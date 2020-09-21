import socket
import os
import asyncio


def get_filename(filename):
    '''
    handle collisions of filename

    :param filename: desireded filename
    :return: string with actual filename
    '''
    name, extension = filename.rsplit(".", 1)
    if not os.path.exists(f"{name}.{extension}"):
        return filename
    else:
        i = 0
        while os.path.exists(f"{name}_copy{i}.{extension}"):
            i += 1
        return f"{name}_copy{i}.{extension}"


async def handle_client(reader: asyncio.StreamReader, writer):
    '''
    handle client connection and save file

    :param reader: StreamReader to receive data from client
    :param writer: StreamWriter to send data to client
    :return:
    '''
    data = await reader.read(256)

    # filename cannot contain newline symbol, so we can use
    # it to separate filename from the rest of the content
    filename, file_content = data.decode().split('\n', 1)
    filename = get_filename(filename)
    print(f"saving as {filename}")

    assert not os.path.exists(filename)
    file = open(filename, "w")

    data = await reader.read(256)
    data = file_content + data.decode()
    while data:
        file.write(data)
        data = await reader.read(256)
        data = data.decode()

    file.close()
    print("Close the connection")
    writer.close()


async def main():
    TCP_IP = socket.gethostbyname(socket.gethostname())
    TCP_PORT = 8800

    server = await asyncio.start_server(handle_client, TCP_IP, TCP_PORT)
    addr = server.sockets[0].getsockname()
    print(addr)
    print(f"server started, waiting for the files")

    async with server:
        await server.serve_forever()


if __name__ == '__main__':
    asyncio.run(main())
