"""Matchstick task"""
import re

"""Matchstick converting lists"""
internal_change_dict = {0: [6, 9], 2: [3], 3: [2, 5], 5: [3], 6: [0, 9], 9: [0, 6]}
take_dict = {6: [5], 7: [1], 8: [0, 6, 9], 9: [3]}
give_dict = {0: [8], 1: [7], 3: [9], 5: [6], 6: [8], 9: [8]}


class Expression:

    def __init__(self, number_list, sign):
        self.number_list = number_list
        self.sign = sign


    @classmethod
    def from_in_list(cls, in_list):
        number_list = [int(in_list[0]), int(in_list[2]), int(in_list[4])]
        sign = in_list[1]
        return cls(number_list, sign)

    def to_string(self):
        return f'{self.number_list[0]}{self.sign}{self.number_list[1]}={self.number_list[2]}'

    def exp_valid(self) -> bool:
        num1 = self.number_list[0]
        num2 = self.number_list[1]
        num3 = self.number_list[2]

        if self.sign == '+':
            if num1 + num2 == num3:
                return True
        elif self.sign == '-':
            if num1 - num2 == num3:
                return True
        return False

    def copy(self):
        return Expression(self.number_list.copy(), self.sign)


def internal_change_in_number(expression: Expression, i) -> Expression:  # index: '0', '1', '2'
    new_expression = expression.copy()
    number = expression.number_list[i]

    for value in internal_change_dict.get(number, []):
        new_expression.number_list[i] = value
        if new_expression.exp_valid():
            return new_expression


def give_stick_to_number(expression: Expression):
    new_expression = expression.copy()
    new_expression.sign = '-'  # changing sign to '-', give matchstick to one of the number
    return stick_exchange(new_expression, give_dict)


def take_stick_from_number(expression: Expression):
    new_expression = expression.copy()
    new_expression.sign = '+'  # change sign to '+', take matchstick from one of the numbers
    return stick_exchange(new_expression, take_dict)


def stick_exchange(expression: Expression, check_dict):
    result_list = []

    for i, number in enumerate(expression.number_list):
        if number in check_dict:
            legit_list = check_dict[number]

            for value in legit_list:
                expression.number_list[i] = value
                if expression.exp_valid():
                    result_list.append(expression.copy())

                # Return to initial state for check_list
                expression.number_list[i] = number

    return result_list


def number_to_number_stick_exchange(expression: Expression):
    new_expression = expression.copy()
    result_list = []

    for i, num1 in enumerate(new_expression.number_list):
        if num1 in take_dict:
            num1_legit_list = take_dict[num1]
            for k, num2 in enumerate(new_expression.number_list):
                if k != i:
                    if num2 in give_dict:
                        num2_legit_list = give_dict[num2]

                        for num1_value in num1_legit_list:
                            new_expression.number_list[i] = num1_value
                            for num2_value in num2_legit_list:
                                new_expression.number_list[k] = num2_value
                                if new_expression.exp_valid():
                                    result_list.append(new_expression.copy())
                                # Return to initial state for check_list
                                new_expression.number_list[k] = num2
                            new_expression.number_list[i] = num1

    return result_list


def get_results(results, expression_list):
    for result_list in expression_list:
        results.append(result_list.to_string())
    return results


def main_function(input_string):
    final_results = []
    input_list = list(input_string)  # first number, sign, second number, equal sign, third number

    expression = Expression.from_in_list(input_list)

    if expression.sign == '-':
        new_expression = Expression(expression.number_list[1:]+expression.number_list[:1], expression.sign)
        if new_expression.exp_valid():  # move equal to the left
            final_results.append(f'{expression.number_list[0]}={expression.number_list[1]}-{expression.number_list[2]}')

        get_results(final_results, take_stick_from_number(expression))  # give matchstick from number to minus sign

    if expression.sign == '+':
        get_results(final_results, give_stick_to_number(expression))  # give matchstick from plus sign to number

    for index in range(3):
        res_list = internal_change_in_number(expression, index)  # matchstick exchange in number itself
        if res_list:
            final_results.append(res_list.to_string())
            # final_results.append(f'{res_list[0]}{res_list[1]}{res_list[2]}={res_list[4]}')

    get_results(final_results, number_to_number_stick_exchange(expression))  # matchstick exchange between numbers
    print(final_results)
    return final_results


if __name__ == '__main__':
    while True:
        input_str = input('Enter expression in format "number1+number2=number3" OR "number1-number2=number3":\n'
                          'For Quit, input: "quit"\n')
        if input_str == 'quit':
            break

        if not re.match(r'[0-9][+-][0-9]=[0-9]', input_str):
            print('Enter valid expression!')
            continue

        f_results = main_function(input_str)
        if f_results:  # print final results
            print('Results: ', f_results)
        else:
            print('No results!\n')
