from smallcalc import calc_parser as cpar
from smallcalc import calc_visitor as cvis


def main():
    p = cpar.CalcParser()
    v = cvis.CalcVisitor()

    while True:
        try:
            text = input('smallcalc :> ')
            p.lexer.load(text)

            node = p.parse_integer()
            res = v.visit(node.asdict())

            print(res)

        except EOFError:
            print("Bye!")
            break

        if not text:
            continue


if __name__ == '__main__':
    main()
