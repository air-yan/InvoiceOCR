import pdf
import ocr
import extract_amount
import extract_id

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
    # return extract_amount.leven_amount(txt)
    return extract_id.leven_invoice_no(txt)
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
        df.loc[:, 'rating'].astype(float)
        # df.loc[:, ['result', 'rating']].astype(float)
        agg_df = df.copy()
        agg_df['rating'] = df.apply(balance_rating_up, axis=1)
        agg_df['rating'] = df.apply(ocr_rating_down, axis=1)

        agg_df = (df.groupby('result')
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
f = open('log.md', 'wb')

# set your working directory
directory = 'd:/git/Invoice-Receipt-OCR/'
dir_test_img = directory + 'test_image/'

# reference for pdfminer looping. This matters a lot!
argu = [(5, 0.5, 5), (100, 1, 5), (5, 1.5, 1.5)]
argu2 = ['1', '3', '6']

# main loop
def main_loop(pdf_process=True, ocr_process=True):
    csv = pd.DataFrame()
    for filename in os.listdir(dir_test_img):
        dir_file = "".join([dir_test_img, filename])
        f.write('Analysing pdf {}...\n'.format(filename).encode('utf8'))

        # If it's a pdf file, then...
        if filename.endswith(".pdf"):
            if pdf_process:
                # **************************************pdfminer process starts
                f.write('\nStarting PDFminer process...\n'.encode('utf8'))

                counter = 1
                df = pd.DataFrame()

                # Perform PDF Miner process:
                # Looping three times with different settings
                for i, j, k in argu:
                    f.write('Performing option {} for pdfminer\n'.format(
                        counter).encode('utf8'))
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

            if ocr_process:
                # **************************************ocr process starts
                f.write('\nStarting ocr process...\n'.encode('utf8'))
                counter = 1
                for i in argu2:
                    f.write('Performing option {} for ocr\n'.format(
                        counter).encode('utf8'))
                    txt = ocr.ocr_process(dir_file, page_seg_method=i)
                    tem_df = regex_extraction(txt)

                    if (tem_df is not None) and (len(tem_df) != 0):
                        tem_df.loc[:, "Process"] = "OCR process {}".format(counter)

                    # Append all DataFrames from the above processes together
                    df = df.append(tem_df)
                    counter += 1
                # **************************************ocr process ends
            # print initial rating
            df = df.loc[:, ['Process', 'Criteria', 'string', 'result', 'rating']]
            f.write('\nThe initial rating is:\n'.encode('utf8'))
            f.write(tabulate(df.sort_values(by='rating'), tablefmt='psql',
                            headers=('Process', 'Criteria', 'string', 'result', 'rating')).encode('utf8'))

            # aggregate ratings based on amount
            # do some ajustment on ratings
            # print final aggregated rating
            agg_df = agg_dfs(df)

            f.write('\nThe final aggregated rating is:\n'.encode('utf8'))
            f.write(tabulate(agg_df, tablefmt='psql', showindex=False,
                            headers=('result', 'frequency', 'final rating')).encode('utf8'))
                

            if len(agg_df) != 0:
                agg_df.loc[:, "File Name"] = filename
                csv = csv.append(agg_df.iloc[0, :])

        else:  # if it's not a pdf file, we do nothing... currently
            #         txt = ocr_process('test_image/' + filname)
            #         regex_extraction(txt)
            pass

        f.write(("-"*20 + "\n\n").encode('utf8'))
    f.close()
    csv.loc[:, ['File Name', 'result']].to_csv("csv_result.csv", index=False)

    print(datetime.now() - startTime)
    # --------------Main Loop-------------- #


if __name__ == "__main__":
    main_loop(ocr_process=False)
