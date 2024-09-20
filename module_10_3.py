from random import randint
from time import sleep
import threading


'''Особо важно соблюсти верную блокировку: 
 в take замок закрывается, в deposit открывается'''
class Bank:

    def __init__(self):
        self.balance = 0
        self.lock = threading.Lock()


    def take(self):
        for _ in range(100):
            summ = randint(50,500)
            print(f'Запрос на  {summ}')
            if summ <= self.balance:
                self.balance = self.balance - summ
                sleep(0.001)
                print(f'Снятие: {summ}. Баланс: {self.balance}')
            else:
                print('Запрос отклонён, недостаточно средств')
                self.lock.acquire()


    def deposit(self):
        for _ in range(100):
            summ = randint(50,500)
            self.balance = self.balance + summ
            sleep(0.001)
            print(f'Пополнение: {summ}. Баланс: {self.balance}')
            if self.balance >= 500 and self.lock.locked():
                self.lock.release()



bk = Bank()

# Т.к. методы принимают self, в потоки нужно передать сам объект класса Bank
th1 = threading.Thread(target=Bank.deposit, args=(bk,))
th2 = threading.Thread(target=Bank.take, args=(bk,))

th1.start()
th2.start()
th1.join()
th2.join()

print(f'Итоговый баланс: {bk.balance}')