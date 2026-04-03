from finance import PersonalFinanceManager
from forecast import monthly_forecast, print_forecast
from colorama import init, Fore, Style

init(autoreset=True)

def main():
    manager = PersonalFinanceManager("data.json")

    while True:
        print(Fore.CYAN + "\n--- Меню ---")
        print(Fore.YELLOW + "1." + Style.RESET_ALL + " Додати дохід")
        print(Fore.YELLOW + "2." + Style.RESET_ALL + " Додати витрату")
        print(Fore.YELLOW + "3." + Style.RESET_ALL + " Показати баланс")
        print(Fore.YELLOW + "4." + Style.RESET_ALL + " Показати всі транзакції")
        print(Fore.YELLOW + "5." + Style.RESET_ALL + " Прогноз витрат")
        print(Fore.YELLOW + "6." + Style.RESET_ALL + " Вихід")
        
        choice = input(Fore.GREEN + "Виберіть дію: ")

        if choice == "1":
            manager.add_income()
        elif choice == "2":
            manager.add_expense()
        elif choice == "3":
            balance = manager.get_balance()
            print(Fore.MAGENTA + f"\nВаш баланс: {balance:,.2f} ₴")
        elif choice == "4":
            manager.view_finances()
        elif choice == "5":
            forecast = monthly_forecast(manager.data, months=1)
            print_forecast(forecast)
        elif choice == "6":
            print(Fore.CYAN + "Дякую за користування програмою. До зустрічі!")
            break
        else:
            print(Fore.RED + "Невірний вибір. Спробуйте ще раз.")

if __name__ == "__main__":
    main()