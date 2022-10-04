import re

"""
mov +
inc +
dec +
add +
sub +
mul +
div +
jmp
cmp
je
jne
jg
jge
jl
jle
call
ret
msg
end
"""


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
    return label[-1] == ':' and label[0].isalpha()


def interpret(lines):
    def find_labels():
        res = {}

        for p, ln in enumerate(lines):
            match re.split(r" +|, +", ln.strip()):
                case [lbl] if islabel(lbl):
                    res[lbl] = p
                case [lbl, *_] if islabel(lbl):
                    error("Syntax", "Invalid label syntax!")
                case _:
                    continue

        return res

    def error(kind, message):
        print(f"{kind} error on line {pointer + 1}:\n >>> {line}\n{message}")
        raise StateException("badabing", registry, kind)

    registry = {}
    pointer = 0
    labels = find_labels(lines)

    while True:
        line = lines[pointer]

        match re.split(r" +|, +", line.strip()):
            # mov, move a value of either a constant or a registry to a registry
            case ["mov", dest, const] if isnumber(const):
                registry[dest] = number(const)
            case ["mov", dest, src]:
                if src in registry:
                    registry[dest] = registry[src]
                else:
                    error("Registry", f"Variable '{src}' does not exist in the registry.")
            case ["mov", *_]:
                error("Syntax", f"Invalid 'mov' syntax!")

            # inc, increase the value of a registry by 1
            case ["inc", dest]:
                if dest in registry:
                    registry[dest] += 1
                else:
                    error("Registry", f"Variable '{dest}' does not exist in the registry.")
            case ["inc", *_]:
                error("Syntax", f"Invalid 'inc' syntax!")

            # dec, decrease the value of a registry by 1
            case ["dec", dest]:
                if dest in registry:
                    registry[dest] -= 1
                else:
                    error("Registry", f"Variable '{dest}' does not exist in the registry.")
            case ["dec", *_]:
                error("Syntax", f"Invalid 'dec' syntax!")

            # add, adds either a registry and a number, or two registries, and stores it in the first registry
            case ["add", dest, const] if isnumber(const):
                if dest in registry:
                    registry[dest] += number(const)
                else:
                    error("Registry", f"Variable '{dest}' does not exist in the registry.")
            case ["add", dest, other]:
                if dest not in registry:
                    error("Registry", f"Variable '{dest}' does not exist in the registry.")
                elif other not in registry:
                    error("Registry", f"Variable '{other}' does not exist in the registry.")
            case ["add", *_]:
                error("Syntax", f"Invalid 'add' syntax!")

            # sub, subtracts either a registry and a number, or two registries, and stores it in the first registry
            case ["sub", dest, const] if isnumber(const):
                if dest in registry:
                    registry[dest] -= number(const)
                else:
                    error("Registry", f"Variable '{dest}' does not exist in the registry.")
            case ["sub", dest, other]:
                if dest not in registry:
                    error("Registry", f"Variable '{dest}' does not exist in the registry.")
                elif other not in registry:
                    error("Registry", f"Variable '{other}' does not exist in the registry.")
            case ["sub", *_]:
                error("Syntax", f"Invalid 'sub' syntax!")

            # mul, multiplies either a registry and a number, or two registries, and stores it in the first registry
            case ["mul", dest, const] if isnumber(const):
                if dest in registry:
                    registry[dest] *= number(const)
                else:
                    error("Registry", f"Variable '{dest}' does not exist in the registry.")
            case ["mul", dest, other]:
                if dest not in registry:
                    error("Registry", f"Variable '{dest}' does not exist in the registry.")
                elif other not in registry:
                    error("Registry", f"Variable '{other}' does not exist in the registry.")
            case ["mul", *_]:
                error("Syntax", f"Invalid 'mul' syntax!")

            # div, adds either a registry and a number, or two registries, and stores it in the first registry
            case ["div", dest, const] if isnumber(const):
                if dest in registry:
                    registry[dest] /= number(const)
                else:
                    error("Registry", f"Variable '{dest}' does not exist in the registry.")
            case ["div", dest, other]:
                if dest not in registry:
                    error("Registry", f"Variable '{dest}' does not exist in the registry.")
                elif other not in registry:
                    error("Registry", f"Variable '{other}' does not exist in the registry.")
            case ["div", *_]:
                error("Syntax", f"Invalid 'div' syntax!")

            # jmp, jump to a given label
            case ["jmp", label]:
                if label in labels:
                    pointer = labels[label]
                    continue
                else:
                    error("Label", f"Label '{label}' is not defined in the program!")
            case ["jmp", *_]:
                error("Syntax", "Invalid 'jmp' syntax!")

            # end, ends the program
            case ["end", *_]:
                break

        pointer += 1

    return registry


if __name__ == '__main__':
    with open("test.asm") as file:
        ls = file.readlines()

    try:
        interpret(ls)
    except Exception:
        pass
