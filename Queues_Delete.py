import pika
from pyrabbit.api import Client

user_host = input("Please enter ampq URI: ")
user_name = input("Please enter username: ")
user_password = input("Please enter password: ")

connection = pika.BlockingConnection(pika.ConnectionParameters(host=user_host)) # Insert host
channel = connection.channel()

cl = Client(user_host, user_name, user_password)
# cl = Client('localhost:15672', 'guest', 'guest')
queues = [q['name'] for q in cl.get_queues()]
print(queues)

queues_without_messages = []
queues_with_messages = []
queues_without_consumers = []

for queue_name in queues:
    queue_state = channel.queue_declare(queue=queue_name, passive=True, durable=True)
    if queue_state.method.message_count == 0:
        queues_without_messages.append(queue_name)
    if queue_state.method.message_count > 0:
        queues_with_messages.append(queue_name)
    if queue_state.method.consumer_count == 0:
        queues_without_consumers.append(queue_name)

print("1. Queues without messages: ", len(queues_without_messages), queues_without_messages)
print("2. Queues with messages: ", len(queues_with_messages), queues_with_messages)
# print("3. Queues without consumers: ", len(queues_without_consumers))
print("3. Total queues: ", len(queues))
print("4. Clear all messages from all queues")


answer = input("Which queues would you like to delete? (1/2/3/4): ")
if int(answer) == 1:
    for queue_name in queues_without_messages:
        channel.queue_delete(queue=queue_name)
elif int(answer) == 2:
    for queue_name in queues_with_messages:
        channel.queue_delete(queue=queue_name)
# elif int(answer) == 3:
#     for queue_name in queues_without_consumers:
#         channel.queue_delete(queue=queue_name)
elif int(answer) == 3:
    for queue_name in queues:
        channel.queue_delete(queue=queue_name)
elif int(answer) == 4:
    for queue_name in queues_with_messages:
        channel.queue_purge(queue=queue_name)
else:
    print("Canceled")
