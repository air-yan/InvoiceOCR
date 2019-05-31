import re
import pandas as pd
from Levenshtein import distance

'''
其他模块负责通过OCR或PDFminer爬取出invoice中的所有string。
这个模块的作用是，从这些爬取出来的string中，提取出具有总金额特征的string。
'''

def regex_parsser(regex_expression, scoring_string):
    '''
    给定一个regex表达式，提取出金额数，同时给该结果打分。
    '''

    string_found_in_list = re.findall(regex_expression, txt, re.IGNORECASE)

    if len(string_found_in_list) == 0:
        print('Nothing matched')

    else:
        for ind, item in enumerate(regex_findall):
            tax_in_string = 'tax' in item.lower()
            last_in_string = 'last' in item.lower()
            if  tax_in_string or last_in_string:
                del regex_findall[ind] # 首先，做一下小修改，删除带有tax和last的部分
            else:
                amount_found_in_list = re.search('[0-9]{1,15}.{1,15}[0-9]{2}', item)

                if amount_found_in_list is not None:

                    score = distance(scoring_string, item.lower())

                    amount = amount_found_in_list.group(0).replace(',', '') # 如果有千分号，替换一下。

                    return amount, score




def leven_amount(txt):
    '''
    This is a warpper for amount_checker.
    In here, three kinds of amount are checked.
    '''
    amount_str_ls = re.findall(
        '(?<!Tax )(?<!Sub)(?<!Sub )(Total[^0-9]{1,30}[0-9,]*\.\d\d)', txt, re.IGNORECASE)
    amount_df = amount_checker(amount_str_ls, "Total: USD \$%d.%d".lower())

    balance_str_ls = re.findall(
        '(?<!Previous )(?<!Prior )(?<!Ending )(?<!Past Due )(Balance[^0-9]{1,30}[0-9,]*\.\d\d)', txt, re.IGNORECASE)
    balance_df = amount_checker(
        balance_str_ls, "Balance due: USD \$%d.%d".lower())

    due_str_ls = re.findall(
        '(Amount Due[^0-9]{1,30}[0-9,]*\.\d\d)', txt, re.IGNORECASE)
    due_df = amount_checker(due_str_ls, "Amount due: USD \$%d.%d".lower())

    # add a column for each one above
    if len(amount_df) != 0:
        amount_df.loc[:, "Criteria"] = "Amount"
    if len(balance_df) != 0:
        balance_df.loc[:, "Criteria"] = "Balance"
    if len(due_df) != 0:
        due_df.loc[:, "Criteria"] = "Due"

    # append them all
    df = amount_df.append([balance_df, due_df])

#     print("amount analysis end")

    return df


def amount_checker(regex_findall, distance_str):
    '''
    This is the function to check for amount,
    based on different criteria.

    1. regex criteria
    2. levenshtein rating criteria

    return a dataframe
    '''
    counter = 0

    df = pd.DataFrame(columns=['string', 'Amount', 'rating'])

    for ind, item in enumerate(regex_findall):
        if ('tax' in item.lower()) or ('last' in item.lower()):
            del regex_findall[ind]
        else:
            amount = re.search('[0-9]{1,15}.{1,15}[0-9]{2}', item)

            if amount is not None:

                rating = distance(distance_str, item.lower())

                amount = amount.group(0).replace(',', '')

                # record it in the dataframe
                df.loc[counter] = [item, amount, rating]
                df[['Amount', 'rating']] = df.loc[:, [
                    'Amount', 'rating']].astype(float)

                # if the amount is 0, we drop it. It's false.
                df = df[df['Amount'] != 0]
                counter += 1

    return df



