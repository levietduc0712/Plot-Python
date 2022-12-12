def main():
    print("This program computers the average of three exam scores.")

    score1, score2, score3 = eval(input("Enter three scores separated by a comma: "))
    average = (score1 + score2 + score3)/3

    print("The average of the score is: ",average)

main()
