import socket
import logging
from tabulate import tabulate
import Templates
logging.basicConfig(format="%(asctime)s|%(levelname)s|%(message)s")

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)   # Используется IPv4, TCP
server_socket.bind(('localhost', 5000))
server_socket.listen()  # Прослушка

# Создаем таблицу
table = tabulate(
    tabular_data=[('Egor', 45), ('Pavel', 12), ('Valik', 0)],
    headers=['user', 'hours'],
    tablefmt='HTML'
)

VIEWS = {
    '/main': b'HTTP/1.1 200 OK\n\n' + Templates.main,
    '/shop': b'HTTP/1.1 200 OK\n\n' + Templates.shop,
    '/users': b'HTTP/1.1 200 OK\n\n' + table.encode('utf-8')    # Обязательно кодируем отправные данные
}


def ger_response(request):
    """ Функция ответа """
    if request:
        url = request[0].split()
        if len(url) > 1:
            url = url[1]        # Вытаскиваем адрес страницы из массива заголовков
        else:
            logging.error('URL is empty')
            return
        if url == '/favicon.ico':
            logging.error('/favicon.ico')
            return
        else:
            return VIEWS.get(url, b'HTTP/1.1 404 Not found\n\n<h1>Not found 404</h1>')


def sender(client, response):
    """Проверка наличия ответа"""
    if response:
        client.sendall(response)
    client.close()


while True:
    client, addr = server_socket.accept()  # Клиент, адрес (ip, порт)
    logging.warning(f'accept client by addr {addr}')
    msg = client.recv(2048)     # Посмотреть что прислано, ограничение в 2048 байт
    request = msg.decode('utf-8').split('\n')
    response = ger_response(request)
    sender(client, response)    # Прислать клиенту ответ
    client.close()