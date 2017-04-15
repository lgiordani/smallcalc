def main():
    while True:
        try:
            text = input('smallcalc :> ')
        except EOFError:
            print("Bye!")
            break

        if not text:
            continue

        print(text)


if __name__ == '__main__':
    main()
