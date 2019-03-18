import pdf
import ocr
import extract_amount

from datetime import datetime
import os
import numpy as np
import pandas as pd
from tabulate import tabulate
import warnings
warnings.filterwarnings("ignore")


def regex_extraction(txt):
    '''
    This controls what functions will be run.
    You can use this to test each function independently.
    '''
    return extract_amount.leven_amount(txt)
#     reg_amount(txt)
#     regex_date(txt)
#     regex_vendor_address(txt)
#     regex_remittance(txt)

# ---------------rate adjustment-------------- #


def balance_rating_up(x):
    if x['Criteria'] == 'Balance':
        return x['rating'] + 2
    else:
        return x['rating']


def ocr_rating_down(x):
    if x['Process'] == 'OCR process':
        return x['rating'] - 3
    else:
        return x['rating']
# ---------------rate adjustment-------------- #


def agg_dfs(df):
    '''This aggregate dfs for different processes together'''
    if len(df) > 1:
        df.loc[:, ['amount', 'rating']].astype(float)
        agg_df = df.copy()
        agg_df['rating'] = df.apply(balance_rating_up, axis=1)
        agg_df['rating'] = df.apply(ocr_rating_down, axis=1)

        agg_df = (df.groupby('amount')
                  .aggregate({'string': len, 'rating': np.mean})
                  .sort_values(by='rating', ascending=True)
                  .reset_index())
        agg_df.loc[:, 'string'].astype(float)
        agg_df['final rating'] = agg_df['rating'] - (agg_df['string'] - 1)
        agg_df.drop('rating', axis=1, inplace=True)
        return agg_df
    else:
        return df


# --------------Main Loop-------------- #
startTime = datetime.now()

# set your working directory
directory = 'D:/git/Invoice-Receipt-OCR/'
dir_test_img = directory + 'test_image/'

# reference for pdfminer looping. This matters a lot!
argu = [(5, 0.5, 5), (100, 1, 5), (5, 1.5, 1.5)]
argu2 = ['1', '3', '6']

# main loop
for filename in os.listdir(dir_test_img):
    dir_file = "".join([dir_test_img, filename])
    print('Analysing pdf {}...'.format(filename))

    # If it's a pdf file, then...
    if filename.endswith(".pdf"):
        # **************************************pdfminer process starts
        print('\nStarting PDFminer process...')

        counter = 1
        df = pd.DataFrame()

        # Perform PDF Miner process:
        # Looping three times with different settings
        for i, j, k in argu:
            print('Performing option {} for pdfminer'.format(counter))
            txt = pdf.convert_pdf(
                dir_file, char_margin=i, line_margin=j, boxes_flow=k)
            tem_df = regex_extraction(txt)

            # Add a column to tem_df to show it's from PDFminer process
            if (tem_df is not None) and (len(tem_df) != 0):
                tem_df.loc[:, "Process"] = "PDF Miner option {}".format(
                    counter)

            # Append all DataFrames together
            df = df.append(tem_df)
            counter += 1
        # **************************************pdfminer process ends

        # **************************************ocr process starts
        print('\nStarting ocr process...')
        counter = 1
        for i in argu2:
            print('Performing option {} for ocr'.format(counter))
            txt = ocr.ocr_process(dir_file, page_seg_method=i)
            tem_df = regex_extraction(txt)

            if (tem_df is not None) and (len(tem_df) != 0):
                tem_df.loc[:, "Process"] = "OCR process {}".format(counter)

            # Append all DataFrames from the above processes together
            df = df.append(tem_df)
            counter += 1

        # print initial rating
        df = df.loc[:, ['Process', 'Criteria', 'string', 'amount', 'rating']]
        print('\nThe initial rating is:')
        print(tabulate(df.sort_values(by='rating'), tablefmt='psql',
                       headers=('Process', 'Criteria', 'string', 'amount', 'rating')))

        # aggregate ratings based on amount
        # do some ajustment on ratings
        # print final aggregated rating
        agg_df = agg_dfs(df)

        print('\nThe final aggregated rating is:')
        print(tabulate(agg_df, tablefmt='psql', showindex=False,
                       headers=('amount', 'frequency', 'final rating')))
        # **************************************ocr process ends

    else:  # if it's not a pdf file
        #         txt = ocr_process('test_image/' + filname) # We use a OCR process
        #         regex_extraction(txt)
        pass

    print("-"*20 + "\n")


print(datetime.now() - startTime)
# --------------Main Loop-------------- #
