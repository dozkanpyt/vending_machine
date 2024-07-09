import os
from beverage import Beverage
from coin import Coin
import turtle


class VendingMachine:
    def __init__(self):
        self.beverages = []
        self.coins = []
        self.total_money = 0
        self.load_data()
        # self.maintain_password = os.environ.get('maintain_password')
        self.maintain_password = '1234'
        self.setup_vending_screen()

    def load_data(self):
        if os.path.exists('prices.txt'):
            with open('prices.txt', 'r') as prices_file:
                for line in prices_file:
                    name, number, price = line.strip().split(',')
                    self.beverages.append(Beverage(name, int(number), float(price)))

        if os.path.exists('coins.txt'):
            with open('coins.txt', 'r') as coins_file:
                for line in coins_file:
                    coin_values = line.strip().split(',')
                    self.coins = [Coin(
                        float(value.replace('c', '')) if 'c' in value else float(value.replace('$', '') * 100) for value
                        in coin_values)]

    def setup_vending_screen(self):
        self.screen = turtle.Screen()
        self.screen.title('Vending Machine')
        self.screen.setup(width=600, height=800)

        self.vending_window = turtle.Turtle()
        self.vending_window.hideturtle()
        self.vending_window.penup()

    def display_beverages(self):

        self.vending_window.clear()
        self.vending_window.goto(-250, 250)
        self.vending_window.write('Available Beverages:', align='left', font=('Arial', 16, 'bold'))
        y_offset = 220
        for beverage in self.beverages:
            if beverage.number > 0:
                self.vending_window.goto(-250, y_offset)
                self.vending_window.write(f'{beverage.name} - ${beverage.price:.2f}', font=('Arial', 14, 'normal'))
                y_offset -= 30

    def input_coins(self):
        self.vending_window.clear()
        self.vending_window.goto(-250, 250)
        self.vending_window.write('Insert Coins:', align='left', font=('Arial', 16, 'bold'))
        total_inserted = 0

        while True:
            coin_text = self.screen.textinput('Insert Coin',
                'Enter Coin(Enter to Done to Finish) (Only Allowed Type: 2$,1$, 50c,25c,10c,5c,1c)')
            if coin_text.lower() == 'done':
                break

            try:
                value = float(coin_text.replace('c', '')) if 'c' in coin_text else float(
                    coin_text.replace('$', '')) * 100
                if value in [coin.value for coin in self.coins]:
                    total_inserted += value
                    self.vending_window.clear()
                    self.vending_window.goto(-250, 250)
                    self.vending_window.write(
                        'Insert Coin(Enter to Done to Finish) (Only Allowed Type: 2$,1$, 50c,25c,10c,5c,1c)')
                    self.vending_window.goto(-250, 220)
                    self.vending_window.write(f'Total Money Inserted: ${total_inserted}/100:.2f', align='left',
                                              font=('Arial', 14, 'bold'))

                else:
                    self.vending_window.goto(-250, 220)
                    self.vending_window.write(f'Invalid Coin: ${value}', align='left', font=('Arial', 16, 'bold'))

            except ValueError:
                self.vending_window.goto(-250, 220)
                self.vending_window.write('Invalid Input', align='left', font=('Arial', 16, 'bold'))

        return total_inserted

    def update_prices_file(self, selected_beverage):
        with open('prices.txt', 'r') as file_prices:
             lines = file_prices.readline()
        for i, line in enumerate(lines):
            if line.startswith(selected_beverage):
                index = line.strip().split(',')
                index[1] = str(selected_beverage.number)
                lines[i] = ','.join(index) + '\n'
                break
        with open('prices.txt', 'w') as prices:
            prices.writelines(lines)

    def select_beverages(self, total_inserted):
            while True:
              beverage_name = self.screen.textinput('Select Beverage', 'Enter Beverage Name:')
              selected_beverage = next((bev for bev in self.beverages if bev.name == beverage_name), None)

              if selected_beverage:
                  if total_inserted >= selected_beverage.price*100:
                      self.vending_window.clear()
                      self.vending_window.goto(-250, 250)
                      self.vending_window.write(f'Dispensing Beverage: {selected_beverage.name}', align='left', font=('Arial', 16, 'bold'))
                      selected_beverage.number -= 1
                      self.update_prices_file(selected_beverage)

                      change = total_inserted - selected_beverage.price*100
                      self.vending_window.goto(-250, 220)
                      self.vending_window.write(f'Change: ${selected_beverage.price}', align='left',
                                                font=('Arial', 14, 'normal'))

                      return
                  else:
                      self.vending_window.goto(-250, 250)
                      self.vending_window.write(f'Insufficient Money for Selected Beverage: {total_inserted}', align='left',
                                                font=('Arial', 16, 'bold'))
              else:
                  self.vending_window.goto(-250, 250)
                  self.vending_window.write('Invalid Selection', align='left', font=('Arial', 16, 'bold'))






    def maintenance_menu(self):
        from maintenance import Maintenance
        password = self.screen.textinput('Maintenance Menu', 'Enter Maintenance Password:')
        if password == self.maintain_password:
            maintenance = Maintenance(self)
            maintenance.run()
        else:
            self.vending_window.clear()
            self.vending_window.goto(-250, 250)
            self.vending_window.write('Incorrect Password', align='left', font=('Arial', 16, 'bold'))

    def run(self):
        while True:
            self.vending_window.clear()
            self.vending_window.goto(-250, 250)
            self.vending_window.write('1. Buy Beverage\n2. Maintenance\n 3.Exit', align='left',
                                                font=('Arial', 16, 'bold'))
            choice = self.screen.textinput('Main Menu', 'Enter Your Choice: 1, 2, 3')
            if choice == '1':
                self.display_beverages()
                total_inserted = self.input_coins()
                self.select_beverages(total_inserted)
            elif choice == '2':
                self.maintenance_menu()
            elif choice == '3':
                break
            else:
                self.vending_window.goto(-250, 220)
                self.vending_window.write('Invalid Selection', align='left',
                                                font=('Arial', 16, 'bold'))

        turtle.bye()