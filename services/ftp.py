import logging

ASK_USER = b"USER: "
ASK_PASS = b"PASS: "
DENIED = b"530 Login incorrect\r\n"

async def handle_connection(reader, writer):
    addr = writer.get_extra_info('peername')
    logging.info(f"[FTP] Connection from {addr}")

    try:
        # Ask username
        writer.write(ASK_USER)
        await writer.drain()
        username = await reader.readline()

        # Ask password
        writer.write(ASK_PASS)
        await writer.drain()
        password = await reader.readline()

        logging.info(f"[FTP] Username: {username.decode(errors='ignore').strip()}, Password: {password.decode(errors='>

        # Deny login
        writer.write(DENIED)
        await writer.drain()

    except Exception as e:
        logging.error(f"[FTP] Error: {e}")
