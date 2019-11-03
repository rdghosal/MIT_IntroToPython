import sys


def main():
    """
    Calculates how long it will take the user to purchase her/his dream house
    """
    annual_salary = float(input("Enter the starting annual salary: "))

    total_cost = 1000000
    current_savings = 0
    portion_saved = 0
    semi_annual_raise = .07
    r = 0.04
    
    high = 10000
    low = 0
    months = 0
    epsilon = 100 

    portion_down_payment = 0.25 * total_cost
    investment = (current_savings * r) / 12

    while not abs(portion_down_payment - current_savings) <= epsilon:
        if months > 36:
            print("It is not possible to pay the down payment in three years")
            sys.exit(1)

        portion_saved = (high + low) // 2
        current_savings = investment + annual_salary / 12 * portion_saved 

        months += 1
        if months % 6 == 0:
            annual_salary += annual_salary * semi_annual_raise 

        if current_savings > portion_down_payment:
            high = portion_saved
        elif current_savings < portion_down_payment:
            low = portion_saved

    print(f"Best savings rate: {portion_saved / 100 : 0.4f}")
    print(f"Steps in bisection search: {months}")
    sys.exit(0)


if __name__ == "__main__":
    main()