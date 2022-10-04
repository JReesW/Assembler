import re
import os
os.system("color")


ARITHMETIC_OPERATORS = {
    "add": lambda a, b: a + b,
    "sub": lambda a, b: a - b,
    "mul": lambda a, b: a * b,
    "div": lambda a, b: a / b,
}


COMPARATIVE_OPERATORS = {
    "je": lambda a, b: a == b,
    "jne": lambda a, b: a != b,
    "jg": lambda a, b: a > b,
    "jge": lambda a, b: a >= b,
    "jl": lambda a, b: a < b,
    "jle": lambda a, b: a <= b
}


UNARY_OPERATORS = {
    "inc": 1,
    "dec": -1
}


class StateException(Exception):
    def __init__(self, message, registry, error_kind):
        super().__init__(message)

        self.registry = registry
        self.error_kind = error_kind


def isnumber(num):
    return num.replace('.', '').isdigit()


def number(num):
    if '.' in num:
        return float(num)
    else:
        return int(num)


def islabel(label):
    label = label.strip()
    return label[-1] == ':' and label[0].isalpha()


def interpret(lines):
    def find_labels():
        res = {}

        for p, ln in enumerate(lines):
            if ln.split(';')[0].strip() == "":
                continue

            match re.split(r" +|, +", ln.split(';')[0].strip()):
                case [lbl] if islabel(lbl):
                    res[lbl.replace(':', '')] = p
                case [lbl, *_] if islabel(lbl):
                    nonlocal pointer
                    pointer = p
                    error("Syntax", "Invalid label syntax!")
                case _:
                    continue

        return res

    def error(kind, message):
        print(f"\n\033[91m{kind} error\033[0m on line {pointer + 1}:\n"
              f" \033[36m>>>\033[0m {lines[pointer].strip()}\n{message}")
        raise StateException("badabing", registry, kind)

    def get_value(source):
        if source in registry:
            return registry[source]
        error("Registry", f"Variable '\033[92m{source}\033[0m' does not exist in the registry.")

    def get_label(lbl):
        if lbl in labels:
            return labels[lbl]
        error("Label", f"Label '\033[92m{label}\033[0m' is not defined in the program!")

    registry = {}
    pointer = 0
    labels = find_labels()
    comparison = None
    stack = []

    while True:
        if lines[pointer].strip() == "":
            pointer += 1
            continue

        line = lines[pointer].split(';')[0]

        match re.split(r" +|, +", line.strip()):
            # mov, move a value of either a constant or a registry to a registry
            case ["mov", dest, const] if isnumber(const):
                registry[dest] = number(const)
            case ["mov", dest, src]:
                registry[dest] = get_value(src)

            # inc/dec, increase or decrease the value of a registry by 1
            case [("inc" | "dec") as op, dest]:
                get_value(dest)
                registry[dest] += UNARY_OPERATORS[op]

            # The arithmetic operators, first arg must be a register, as the result will be stored there
            case [("add" | "sub" | "mul" | "div") as op, dest, other]:
                if isnumber(other):
                    registry[dest] = ARITHMETIC_OPERATORS[op](get_value(dest), number(other))
                else:
                    registry[dest] = ARITHMETIC_OPERATORS[op](get_value(dest), get_value(other))

            # jmp, jump to a given label
            case ["jmp", label]:
                pointer = get_label(label)
                continue

            # cmp, sets up a comparison, to be used by the comparative jump commands
            case ["cmp", a, b]:
                a = number(a) if isnumber(a) else get_value(a)
                b = number(b) if isnumber(b) else get_value(b)
                comparison = a, b

            # comparative jump commands
            case [cond, label] if cond in COMPARATIVE_OPERATORS:
                if comparison is not None:
                    if COMPARATIVE_OPERATORS[cond](*comparison):
                        pointer = get_label(label)
                        continue
                else:
                    error("Comparison", "No comparison made before trying to jump!")

            # call a function
            case ["call", label]:
                stack.append(pointer)
                pointer = get_label(label)
                continue

            # return from a function
            case ["ret"]:
                if stack:
                    pointer = stack.pop()
                else:
                    error("Stack", "No pointer on the stack to return to!")

            # print a message
            case ["msg"]:
                error("Syntax", "Invalid '\033[92mmsg\033[0m' syntax!")
            case ["msg", *_]:
                args = line.strip().split(' ', 1)[1].strip()
                parts = []

                cur = ""
                in_str = False

                for c in args:
                    if c == ',' and not in_str:
                        parts.append(cur)
                        cur = ""
                        continue
                    elif c == "'":
                        in_str = not in_str
                    cur += c
                parts.append(cur)

                stripped = [p.strip() for p in parts]
                print("".join(p[1:-1] if p[0] == "'" else str(get_value(p)) for p in stripped))

            # end, ends the program
            case ["end", *_]:
                break

            case [cmd] if islabel(cmd):
                pass

            case [cmd, *_]:
                error("Syntax", f"Invalid '\033[92m{cmd}\033[0m' syntax!")

        pointer += 1

        if pointer == len(lines):
            break

    return registry


if __name__ == '__main__':
    with open("test.asm") as file:
        ls = file.readlines()

    try:
        interpret(ls)
    except StateException as e:
        pass
