
class Maintenance:
    def __init__(self, vending_machine):
        self.vending_machine = vending_machine

    def open_safe(self):
        self.vending_machine.vending_window.clear()
        self.vending_machine.vending_window.goto(-250, 250)
        self.vending_machine.vending_window.write('Safe Contents:',  align='left', font=('Arial', 16, 'bold'))
        total_coins = 0
        y_offset = 220
        for coin in self.vending_machine.coins:
            total_coins += int(coin.value)
            self.vending_machine.vending_window.goto(-250, y_offset)
            self.vending_machine.vending_window.write(f'{coin.value:.2f}', align='left', font=('Arial', 16, 'bold'))
            y_offset -= 30
        self.vending_machine.vending_window.goto(-250, y_offset)
        self.vending_machine.vending_window.write(f'Total $: {total_coins/100:.2f}', align='left', font=('Arial', 16, 'bold'))


    def withdraw_money(self):
       w_money = self.vending_machine.screen.textinput('Withdraw Money', 'Enter Amount of Withdraw Money'))
       withdraw_money = float(w_money.replace('c', '')) if 'c' in w_money else float(w_money.replace('$', '')) * 100
       if withdraw_money <= self.vending_machine.total_money:
           self.vending_machine.vending_window.goto(-250, 250)
           self.vending_machine.vending_window.write(f'Money to Withdraw: ${withdraw_money/100:.2f}', align='left', font=('Arial', 16, 'bold'))
       else:
           self.vending_machine.vending_window.goto(-250, 250)
           self.vending_machine.vending_window.write('Insufficient Amount of Money', align='left',
                                     font=('Arial', 16, 'bold'))


    def run(self):
        while True:
            self.vending_machine.vending_window.clear()
            self.vending_machine.vending_window.goto(-250, 250)
            self.vending_machine.vending_window.write('1. Open Vending Machine Safe\n2.Withdraw Money\n 3.Close Maintenance Menu', align='left',
                                      font=('Arial', 16, 'bold'))
            choice = self.vending_machine.screen.textinput('Main Menu', 'Enter Your Choice: 1, 2, 3')
            if choice == '1':
                self.open_safe()
            elif choice == '2':
                self.withdraw_money()
            elif choice == '3':
                break

            else:
                self.vending_machine.vending_window.goto(-250, 220)
                self.vending_machine.vending_window.write('Invalid Selection', align='left',
                                          font=('Arial', 16, 'bold'))
