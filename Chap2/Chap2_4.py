def main():
    cel = 0
    print("{:<35} {:<25}".format('The temperature in Celcius','The temperature in Fahrenheit'))
    for i in range(10):
        fahrenheit = 9/5 * cel + 32
        print("{:<35} {:<25}".format(cel, fahrenheit))
        cel = cel + 10

main()
