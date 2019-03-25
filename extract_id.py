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

    df = pd.DataFrame(columns=['string', 'ID', 'rating'])

    for ind, item in enumerate(regex_findall):
        tem_string_for_rating = re.sub('\d{1,15}', '%d', item.lower()).replace('invoice number','').replace('invoice no','')
        invoice=re.search('\d.*\d', item)
        
        if invoice is None:
            pass
        elif  len(invoice.group(0)) < 4 or ('.' in invoice.group(0)) or ('date' in item.lower()) or ('usd' in item.lower()) or ('total' in item.lower()) or ('amount' in item.lower()):
            del regex_findall[ind]
        else:
            print(tem_string_for_rating)

            rating=distance(distance_str, tem_string_for_rating)

            invoice=invoice.group(0)

            # record it in the dataframe
            df.loc[counter]=[item, invoice, rating]
            df['rating']=df.loc[:, 'rating'].astype(float)

            counter += 1

    return df


def leven_invoice_no(txt):
    '''
    This is a warpper for invoice_no_checker.
    '''
    id_str_ls=re.findall(
        'invoice[^0-9]{1,15}[^a-zA-Z]{1,20}\d', txt, re.IGNORECASE)
    id_df=invoice_no_checker(id_str_ls, "%d".lower())

    # balance_str_ls = re.findall(
    #     '(?<!Previous )(?<!Prior )(?<!Ending )(?<!Past Due )(Balance[^0-9]{1,30}[0-9,]*\.\d\d)', txt, re.IGNORECASE)
    # balance_df = invoice_no_checker(
    #     balance_str_ls, "Balance due: USD \$%d.%d".lower())

    # due_str_ls = re.findall(
    #     '(Amount Due[^0-9]{1,30}[0-9,]*\.\d\d)', txt, re.IGNORECASE)
    # due_df = invoice_no_checker(due_str_ls, "Amount due: USD \$%d.%d".lower())

    # add a column for each one above
    if len(id_df) != 0:
        id_df.loc[:, "Criteria"]="Invoice"
    # if len(balance_df) != 0:
    #     balance_df.loc[:, "Criteria"] = "Balance"
    # if len(due_df) != 0:
    #     due_df.loc[:, "Criteria"] = "Due"

    # append them all
    df=id_df

#     print("amount analysis end")

    return df
