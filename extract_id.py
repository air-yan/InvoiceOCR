# id extraction tools
import re
import pandas as pd
from Levenshtein import distance


def invoice_no_checker(regex_findall, distance_str):
    '''
    This is the function to check for invoice #,
    based on different criteria.

    1. regex criteria
    2. levenshtein rating criteria

    return a dataframe
    '''
    counter = 0

    df = pd.DataFrame(columns=['string', 'invoice#', 'rating'])

    for ind, item in enumerate(regex_findall):
        if ('tax' in item.lower()) or ('last' in item.lower()):
            del regex_findall[ind]
        else:
            invoice = re.search('\d.*\d', item)

            if invoice is not None:

                rating = distance(distance_str, item.lower())

                # invoice = invoice.group(0).replace('-', '')

                # record it in the dataframe
                df.loc[counter] = [item, invoice, rating]
                df['rating'] = df.loc[:, 'rating'].astype(float)

                counter += 1

# testing code below:
#     if len(regex_findall) > 0:
#         print(tabulate(df.sort_values(by='rating',ascending=True),headers=('string','invoice','rating'),tablefmt='psql'))
#                 print('The string is: {}'.format(item))
#                 print('The invoice is: {}'.format(invoice))
#                 print('The rating is: {}'.format(rating))
#                 print('-'*20)
    return df


def leven_invoice_no(txt):
    '''
    This is a warpper for invoice_no_checker.
    
    '''
    id_str_ls = re.findall(
        'Invoice Number.*\s*\d.*\d', txt, re.IGNORECASE)
    id_df = invoice_no_checker(id_str_ls, "Invoice Number %d".lower())

    # balance_str_ls = re.findall(
    #     '(?<!Previous )(?<!Prior )(?<!Ending )(?<!Past Due )(Balance[^0-9]{1,30}[0-9,]*\.\d\d)', txt, re.IGNORECASE)
    # balance_df = invoice_no_checker(
    #     balance_str_ls, "Balance due: USD \$%d.%d".lower())

    # due_str_ls = re.findall(
    #     '(Amount Due[^0-9]{1,30}[0-9,]*\.\d\d)', txt, re.IGNORECASE)
    # due_df = invoice_no_checker(due_str_ls, "Amount due: USD \$%d.%d".lower())

    # add a column for each one above
    if len(id_df) != 0:
        id_df.loc[:, "Criteria"] = "Invoice"
    # if len(balance_df) != 0:
    #     balance_df.loc[:, "Criteria"] = "Balance"
    # if len(due_df) != 0:
    #     due_df.loc[:, "Criteria"] = "Due"

    # append them all
    df = id_df

#     print("amount analysis end")

    return df
