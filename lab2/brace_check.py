brackets = {
    '(': ')',
    '{': '}',
    '[': ']'
}


def bracket_check(lines):
    stack = []
    for row in range(len(lines)):
        for column in range(len(lines[row])):
            s = lines[row][column]
            if s in brackets.keys():
                stack.append(s)
            elif s in brackets.values():
                if len(stack) == 0 or brackets[stack[-1]] != s:
                    return f'{row}, {column} Bracket error, expected {brackets[stack[-1]]}\n' \
                           f'{row + 1}: {lines[row]}\n' \
                           f'{" " * (len((row + 1).__str__()) + 1 + column)} ^'
                else:
                    stack.pop()

    if len(stack) != 0:
        return f'{len(lines)}, 0 Bracket error, expected {brackets[stack[-1]]}\n' \
               f'{len(lines)}: {lines[len(lines) - 1]}\n' \
               f'{" " * (len((len(lines) - 1).__str__()) + 1)} ^'

    return True
