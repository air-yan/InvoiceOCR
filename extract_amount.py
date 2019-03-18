# string extraction tools
import re
import pandas as pd
from Levenshtein import distance


def amount_checker(regex_findall, distance_str):
    '''
    This is the function to check for amount,
    based on different criteria.

    1. regex criteria
    2. levenshtein rating criteria

    return a dataframe
    '''
    counter = 0

    df = pd.DataFrame(columns=['string', 'amount', 'rating'])

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
                df[['amount', 'rating']] = df.loc[:, [
                    'amount', 'rating']].astype(float)

                # if the amount is 0, we drop it. It's false.
                df = df[df['amount'] != 0]
                counter += 1

# testing code below:
#     if len(regex_findall) > 0:
#         print(tabulate(df.sort_values(by='rating',ascending=True),headers=('string','amount','rating'),tablefmt='psql'))
#                 print('The string is: {}'.format(item))
#                 print('The amount is: {}'.format(amount))
#                 print('The rating is: {}'.format(rating))
#                 print('-'*20)
    return df


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
