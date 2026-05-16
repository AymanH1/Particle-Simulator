#include <iostream>
#include <string>

using namespace std;

class BankAccount {
    public:
        int bank = 1000;
        int cash = 1000;

        void deposit(int amount) {
            if (amount <= cash){
                bank += amount;
                cash -= amount;
            } else {
                cout << "You don't have enough cash to do this!\n";
            }
        }

        void withdraw (int amount) {
            if (amount <= bank) {
                cash += amount;
                bank -= amount;
            } else {
                cout << "You don't have enough money in the bank to do this!\n";
            }
        }
        void check_balance() {
            cout << "You have " << bank << " in the bank\n";
            cout << "You have " << cash << " in cash\n";
        }
};


int main() {
    int option {};
    int amount {};
    BankAccount user1;
    
    do {
        cout << "1)Deposit\n2)Withdraw\n3)Check Balance\n4)Close\n";
        cin >> option;
        if (option == 1) {
            cout << "Enter an amount to deposit: ";
            cin >> amount;
            user1.deposit(amount);
        }
        else if (option == 2) {
            cout << "Enter an amount to withdraw: ";
            cin >> amount;
            user1.withdraw(amount);
        }
        else if (option == 3) {
            user1.check_balance();
        }
    } while (option != 4);
    return 0;
}