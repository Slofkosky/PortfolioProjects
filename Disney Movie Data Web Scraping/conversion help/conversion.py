import re

amounts = r"thousand|million|billion"
number = r"\d+(,\d{3})*\.*\d*"

range_og = rf"\${number}(-|\sto\s|–)({number})\s({amounts})"
range_re1 = rf"\${number}(-|\sto\s|–)"
range_re2 = rf"({number})\s({amounts})"
range_re = rf"{range_re1}{range_re2}"
word_re = rf"\${number}(-|\sto\s)?({number})?\s({amounts})"
value_re = rf"\${number}"


def word_to_value(word):
    value_dict = {"thousand": 1000, "million": 1000000, "billion": 1000000000}
    return value_dict[word]

def value_conversion(string):   
        v_string = re.search(number, string).group()
        value = float(v_string.replace(",", ""))
        return value

def range_value_conversion(string):
    trim = re.findall(range_re2, string, flags=re.I)
    value1 = value_conversion(string)
    value2 = float(trim[0][0])
    return ((value1 + value2)*0.5)

def parse_word_syntax(string):
    value = value_conversion(string)
    word = re.search(amounts, string, flags=re.I).group().lower()
    word_value = word_to_value(word)
    return value*word_value
    
def parse_range_syntax(string):
    value = range_value_conversion(string)
    word = re.search(amounts, string, flags=re.I).group().lower()
    word_value = word_to_value(word)
    return value*word_value

def parse_value_syntax(string):
    return value_conversion(string)

'''
money_conversion("$12.2 million") --> 12200000 # Word syntax
money_conversion("$790,000") --> 790000 ## Value syntax
'''

def money_conversion(money):
    if money == "N/A":
        return None

    if isinstance(money, list):
        money = money[0]

    range_syntax = re.search(range_re,money, flags=re.I)
    word_syntax = re.search(word_re, money, flags=re.I)
    value_syntax = re.search(value_re, money)


    if range_syntax:
        return parse_range_syntax(range_syntax.group())

    if word_syntax:
        return parse_word_syntax(word_syntax.group())

    elif value_syntax:
        return parse_value_syntax(value_syntax.group())
    
    else:
        return None

        
print(money_conversion("$790 million"))
