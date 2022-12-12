def main():
    print("This program calculates the total future value")
    print("of a multi-year investment with by describing")
    print("the interest accrued in terms of a nominal rate")
    print("and the number of compounding periods.")

    principal = eval(input("Enter the initial principal: "))
    interestrate = eval(input("Enter the interest rate: "))
    periods = eval(input("Enter the number of compounding periods per year: "))
    years = eval(input("Enter the number of years for the investment: "))

    nominalrate = interestrate / periods
          
    for i in range(periods * years):
          principal = principal * (1 + nominalrate)

    print("The value in ", years ,"years is:", principal, sep=" ")

main()
