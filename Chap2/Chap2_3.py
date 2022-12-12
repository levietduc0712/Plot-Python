cel1,cel2,cel3,cel4,cel5 = eval(input("Enter 5 temperatures: "))

def main(a,b,c,d,e):
    cel = [a,b,c,d,e]
    for i in range(5):
        fahrenheit = 9/5 * cel[i] + 32
        print("The temperature is",fahrenheit," degress Fahrenheit.")

main(cel1,cel2,cel3,cel4,cel5)
