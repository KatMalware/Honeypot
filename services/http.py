import logging

WELCOME = b"220 Welcome to Fake HTTP Server\r\n"
ASK_USER = b"USER: "
ASK_PASS = b"PASS: "
DENIED = b"530 Login incorrect\r\n"

async def handle_connection(reader, writer):
    addr = writer.get_extra_info('peername')
    logging.info(f"[HTTP] Connection from {addr}")

    try:
        writer.write(WELCOME)
        await writer.drain()

        writer.write(ASK_USER)
        await writer.drain()
        username = await reader.readline()

        writer.write(ASK_PASS)
        await writer.drain()
        password = await reader.readline()

        logging.info(f"[HTTP] Username: {username.decode(errors='ignore').strip()}, Password: {password.decode(errors='ignore').strip()}")

        writer.write(DENIED)
        await writer.drain()

    except Exception as e:
        logging.error(f"[HTTP] Error: {e}")
    finally:
        try:
            writer.close()
            await writer.wait_closed()
        except:
            pass
