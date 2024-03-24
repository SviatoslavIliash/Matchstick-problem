"""Matchstick task"""
import re

"""Matchstick converting lists"""
internal_change_dict = {0: [6, 9], 2: [3], 3: [2, 5], 5: [3], 6: [0, 9], 9: [0, 6]}
take_dict = {6: [5], 7: [1], 8: [0, 6, 9], 9: [3]}
give_dict = {0: [8], 1: [7], 3: [9], 5: [6], 6: [8], 9: [8]}


def exp_valid(in_list):
    num1 = int(in_list[0])
    math_sign = in_list[1]
    num2 = int(in_list[2])
    num3 = int(in_list[4])

    if math_sign == '+':
        if num1 + num2 == num3:
            return True
    elif math_sign == '-':
        if num1 - num2 == num3:
            return True
    return False


def internal_change_in_number(in_list, i):  # index: '0', '2', '4'
    check_list = in_list.copy()
    number = int(in_list[i])

    if number in internal_change_dict:
        legit_list = internal_change_dict[number]
        for value in legit_list:
            check_list[i] = value
            if exp_valid(check_list):
                return check_list
            else:
                check_list[i] = number


def give_stick_to_number(in_list):
    check_list = in_list.copy()
    check_list[1] = '-'  # changing sign to '-', give matchstick to one of the number
    return stick_exchange(check_list, give_dict)


def take_stick_from_number(in_list):
    check_list = in_list.copy()
    check_list[1] = '+'  # change sign to '+', take matchstick from one of the numbers
    return stick_exchange(check_list, take_dict)


def stick_exchange(check_list, check_dict):
    number_list = [int(check_list[0]), int(check_list[2]), int(check_list[4])]
    result_list = []

    for i, number in enumerate(number_list):
        if number in check_dict:
            legit_list = check_dict[number]
            check_i = match_index_func(i)

            for value in legit_list:
                check_list[check_i] = value
                if exp_valid(check_list):
                    result_list.append(check_list.copy())

                # Return to initial state for check_list
                check_list[check_i] = number

    return result_list


def number_to_number_stick_exchange(in_list):
    check_list = in_list.copy()
    number_list = [int(check_list[0]), int(check_list[2]), int(check_list[4])]
    result_list = []

    for i, num1 in enumerate(number_list):
        if num1 in take_dict:
            num1_legit_list = take_dict[num1]
            for k, num2 in enumerate(number_list):
                if k != i:
                    if num2 in give_dict:
                        num2_legit_list = give_dict[num2]
                        check_i = match_index_func(i)
                        check_k = match_index_func(k)
                        for num1_value in num1_legit_list:
                            check_list[check_i] = num1_value
                            for num2_value in num2_legit_list:
                                check_list[check_k] = num2_value
                                if exp_valid(check_list):
                                    result_list.append(check_list.copy())
                                # Return to initial state for check_list
                                check_list[check_k] = num2
                            check_list[check_i] = num1

    return result_list


def match_index_func(i):
    match i:
        case 0:
            return 0
        case 1:
            return 2
        case 2:
            return 4


def get_results(results, result_lists):
    for result_list in result_lists:
        results.append(f'{result_list[0]}{result_list[1]}{result_list[2]}={result_list[4]}')
    return results


def main_function(input_string):
    final_results = []
    input_list = []  # first number, sign, second number, equal sign, third number
    for char in input_string:
        input_list.append(char)

    number1 = int(input_list[0])
    sign = input_list[1]
    number2 = int(input_list[2])
    number3 = int(input_list[4])
    index_list = [0, 2, 4]

    if sign == '-':
        if exp_valid([number2, '-', number3, '=', number1]):  # move equal to the left
            final_results.append(f'{number1}={number2}-{number3}')

        get_results(final_results, take_stick_from_number(input_list))  # give matchstick from number to minus sign

    if sign == '+':
        get_results(final_results, give_stick_to_number(input_list))  # give matchstick from plus sign to number

    for index in index_list:
        res_list = internal_change_in_number(input_list, index)  # matchstick exchange in number itself
        if res_list:
            final_results.append(f'{res_list[0]}{res_list[1]}{res_list[2]}={res_list[4]}')

    get_results(final_results, number_to_number_stick_exchange(input_list))  # matchstick exchange between numbers

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
