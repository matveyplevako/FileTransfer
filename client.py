import asyncio
import sys
import os


# Prints iterations progress
def progress_bar(iteration, total):
    bar_length = int(100 * iteration // total)
    bar = '█' * bar_length + '-' * (100 - bar_length)
    print(f'\r{bar}| {"{0:.1f}".format(100 * (iteration / float(total)))}% ', end='\r')


async def tcp_client(filename, host, port):
    try:
        reader, writer = await asyncio.open_connection(
            host, port)
    except:
        print("Cannot establish connection")
        return

    # send filename to server
    writer.write(filename.encode() + b'\n')
    await writer.drain()

    # send chucks of data to server
    file_size = os.path.getsize(filename)
    sent_size = 0
    progress_bar(0, file_size)
    with open(filename, "rb") as file:
        data = file.read(256)
        while data:
            sent_size += 256
            progress_bar(min(file_size, sent_size), file_size)
            writer.write(data)
            await writer.drain()
            data = file.read(256)

    print()
    print('Close the connection')
    writer.close()
    await writer.wait_closed()


def main():
    try:
        filename, ip, port = sys.argv[1:4]
    except:
        print("Please, provide correct number of arguments: file domain-name|ip-address port-number")
        return

    asyncio.run(tcp_client(filename, ip, port))


if __name__ == '__main__':
    main()
