import datetime

from network_tools import NetworkToolsAPI

api_key = "API_KEY"  # замените на ваш API ключ
client = NetworkToolsAPI(api_key)

user_usage = client.get_usage()

for request in user_usage.response.usage:
    timestamp = datetime.datetime.fromtimestamp(request.timestamp).strftime('%Y-%m-%d %H:%M:%S')
    comment = request.comment
    balance_change = f"{request.balance_change:.8f}"  # Вывод с 8 знаками после запятой
    print(f"{timestamp:<20} {comment:<60} {balance_change:<15}")

print("Баланс:", user_usage.response.balance)  # Отображение оставшегося баланса
