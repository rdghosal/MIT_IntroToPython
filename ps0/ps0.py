from numpy import log2


def main():
    x = input("Enter number x: ")
    y = input("Enter number y: ")

    x = int(x)
    y = int(y)

    print(x ** y)
    print(log2(x))


if __name__ == "__main__":
    main()