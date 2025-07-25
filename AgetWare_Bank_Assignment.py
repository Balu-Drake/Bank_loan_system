class Loan:
    def __init__(self, loan_id, customer_id, P, N, I):
        self.loan_id = loan_id
        self.customer_id = customer_id
        self.P = P
        self.N = N
        self.I = I
        self.A = round(P * (1 + (I * N) / 100), 2)
        self.EMI = round(self.A / (N * 12), 2)
        self.balance = self.A
        self.paid = 0
        self.transactions = []

    def make_payment(self, amount, mode='EMI'):
        self.paid += amount
        self.balance = round(self.A - self.paid, 2)
        self.transactions.append({'mode': mode, 'amount': amount})

    def get_ledger(self):
        emi_left = int(self.balance / self.EMI) if self.EMI else 0
        return {
            'loan_id': self.loan_id,
            'transactions': self.transactions,
            'balance': self.balance,
            'monthly_EMI': self.EMI,
            'EMIs_left': emi_left
        }

    def get_summary(self):
        total_interest = round(self.A - self.P, 2)
        emi_left = int(self.balance / self.EMI) if self.EMI else 0
        return {
            'loan_amount(P)': self.P,
            'Total_amount(A)': self.A,
            'EMI_amount': self.EMI,
            'Total_interest(I)': total_interest,
            'Amount_paid': self.paid,
            'EMIs_left': emi_left
        }

class BankSystem:
    def __init__(self):
        self.loans = {}
        self.customers = {}

    def lend(self, customer_id, P, N, I):
        loan_id = f"{customer_id}_{len(self.customers.get(customer_id, [])) + 1}"
        loan = Loan(loan_id, customer_id, P, N, I)
        self.loans[loan_id] = loan
        self.customers.setdefault(customer_id, []).append(loan_id)
        return {'loan_id': loan_id, 'Total_amount(A)': loan.A, 'Monthly_EMI': loan.EMI}

    def payment(self, loan_id, amount, mode='EMI'):
        if loan_id in self.loans:
            self.loans[loan_id].make_payment(amount, mode)
            return f"Payment of ₹{amount} via {mode} accepted."
        return "Loan ID not found."

    def ledger(self, loan_id):
        return self.loans[loan_id].get_ledger() if loan_id in self.loans else "Loan ID not found."

    def account_overview(self, customer_id):
        overview = []
        for loan_id in self.customers.get(customer_id, []):
            overview.append(self.loans[loan_id].get_summary())
        return overview

def list_customer_loans(bank, customer_id):
    loan_ids = bank.customers.get(customer_id, [])
    if loan_ids:
        print(f"\n📌 Available loans for {customer_id}: {', '.join(loan_ids)} is the loan_id")
    else:
        print(f"\n❌ No loans found for customer {customer_id}")

def main():
    bank = BankSystem()

    while True:
        print("\n🏦 Welcome to the Bank Loan System")
        print("1. LEND a loan")
        print("2. MAKE a payment")
        print("3. CHECK loan ledger")
        print("4. ACCOUNT overview")
        print("5. EXIT")

        choice = input("Enter your choice (1-5): ").strip()

        if choice == '1':
            customer_id = input("Enter Customer ID: ").strip()
            P = float(input("Enter Loan Amount (P): ₹").strip())
            N = float(input("Enter Loan Period (N in years): ").strip())
            I = float(input("Enter Rate of Interest (I %): ").strip())
            result = bank.lend(customer_id, P, N, I)
            print(f"\n✅ Loan created: Loan ID {result['loan_id']}")
            print(f"Total Payable Amount (A): ₹{result['Total_amount(A)']}")
            print(f"Monthly EMI: ₹{result['Monthly_EMI']}")

        elif choice == '2':
            customer_id = input("Enter Customer ID: ").strip()
            list_customer_loans(bank, customer_id)
            loan_id = input("Enter Loan ID: ").strip()
            amount = float(input("Enter Payment Amount: ₹").strip())
            mode = input("Payment mode (EMI or LUMP SUM): ").strip().upper()
            message = bank.payment(loan_id, amount, mode)
            print(f"\n💳 {message}")

        elif choice == '3':
            customer_id = input("Enter Customer ID: ").strip()
            list_customer_loans(bank, customer_id)
            loan_id = input("Enter Loan ID: ").strip()
            ledger = bank.ledger(loan_id)
            if isinstance(ledger, str):
                print(f"\n❌ {ledger}")
            else:
                print(f"\n📜 Loan Ledger for {loan_id}")
                for txn in ledger['transactions']:
                    print(f"- {txn['mode']} payment of ₹{txn['amount']}")
                print(f"Balance: ₹{ledger['balance']}")
                print(f"EMI: ₹{ledger['monthly_EMI']}")
                print(f"EMIs left: {ledger['EMIs_left']}")

        elif choice == '4':
            customer_id = input("Enter Customer ID: ").strip()
            overview = bank.account_overview(customer_id)
            if not overview:
                print(f"\n❌ No loans found for customer {customer_id}")
            else:
                print(f"\n📊 Account Overview for {customer_id}")
                for idx, summary in enumerate(overview, start=1):
                    print(f"\nLoan {idx}:")
                    for key, value in summary.items():
                        print(f"{key}: ₹{value}" if isinstance(value, float) else f"{key}: {value}")

        elif choice == '5':
            print("\n👋 Thank you for using the system.")
            break

        else:
            print("\n⚠️ Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
