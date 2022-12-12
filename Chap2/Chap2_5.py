year = int(input("Enter years: "))

def main(a):
    print("This program calculates the future value")
    print("of a", a,"year investment.")
    principal = eval(input("Enter the initial principal: "))
    apr = eval(input("Enter the annual interest rate: "))

    for i in range(a):
        principal = principal * (1 + apr)
    
    print("The value in",a,"years is ",principal)

main(year)
