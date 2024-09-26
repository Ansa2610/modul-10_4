import time
# Задача "Потоки гостей в кафе":
# Для проверки значения на None используйте оператор is (table.guest is None).
# Для добавления в очередь используйте метод put, для взятия - get.
# Для проверки пустоты очереди используйте метод empty.
# Для проверки выполнения потока в текущий момент используйте метод is_alive.

from threading import Thread
from queue import Queue
from time import sleep
from random import randint


class Table:

	def __init__(self, number):
		self.number = number
		self.guest = None


class Guest(Thread):

	def __init__(self, name):
		super().__init__()
		self.name = name

	def run(self):
		sleep(randint(3, 10))


class Cafe:
	def __init__(self, *tables):
		self.queue = Queue()
		self.tables = list(tables)

	def guest_arrival(self, *guests):
		for guest in guests:
			if any(table.guest is None for table in self.tables):
				for table in self.tables:
					if table.guest is None:
						table.guest = guest
						guest.start()
						print(f'{guest.name} сел(-а) за стол номер {table.number}.')
						break

			else:
				self.queue.put(guest)
				print(f'{guest.name} ожидает в очереди.')

	def discuss_guests(self):
		while not self.queue.empty() or any(table.guest is not None for table in self.tables):
			for table in self.tables:
				if table.guest is not None and not table.guest.is_alive():
					print(f'{table.guest.name} поел(-а) и ушёл(ушла).')
					print(f'Стол номер {table.number} свободен.')
					table.guest = None
					break
			if not self.queue.empty() and any(table.guest is None for table in self.tables):
				for table in self.tables:
					if table.guest is None:
						guest = self.queue.get()
						table.guest = guest
						guest.start()
						print(f'{guest.name} вышел(вышла) из очереди и сел(-а) за стол номер {table.number}')
						break


tables = [Table(number) for number in range(1, 6)]
guests_names = [
			'Maria', 'Anna', 'Asko', 'Barney', 'Dasha', 'Roman',
			'Viktoria', 'Nikita', 'Galina', 'Pavel', 'Ilya', 'Alexandra'
				]

guests = [Guest(name) for name in guests_names]
cafe = Cafe(*tables)
cafe.guest_arrival(*guests)
cafe.discuss_guests()
