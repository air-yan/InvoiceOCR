# import pdf
# import ocr
# import extract_amount
# import extract_id

# from datetime import datetime
# import os
# import numpy as np
# import pandas as pd
# import warnings
# warnings.filterwarnings("ignore")


# def regex_extraction(txt, process):
#     '''
#     This controls what functions will be run.
#     You can use this to test each function independently.
#     '''
#     id_df = extract_id.leven_invoice_no(txt)
#     amount_df = extract_amount.leven_amount(txt)

#     ls = [amount_df, id_df]

#     for df in ls:
#         if (df is not None) and (len(df) != 0):
#             df.loc[:, "Process"] = process

#     return id_df, amount_df
# # ---------------rate adjustment-------------- #


# def balance_rating_up(x):
#     if x['Criteria'] == 'Balance':
#         return x['rating'] + 2
#     else:
#         return x['rating']


# def ocr_rating_down(x):
#     if x['Process'] == 'OCR process':
#         return x['rating'] - 3
#     else:
#         return x['rating']
# # ---------------rate adjustment-------------- #


# def agg_dfs(df, result, filename):
#     '''This aggregate dfs for different processes together'''
#     if len(df) > 1:
#         df.loc[:, 'rating'].astype(float)
#         agg_df = df.copy()
#         agg_df['rating'] = df.apply(balance_rating_up, axis=1)
#         agg_df['rating'] = df.apply(ocr_rating_down, axis=1)

#         agg_df = (df.groupby(result)
#                   .aggregate({'string': len, 'rating': np.mean})
#                   .sort_values(by='rating', ascending=True)
#                   .reset_index())
#         agg_df.loc[:, 'string'].astype(float)
#         agg_df['final rating'] = agg_df['rating'] - (agg_df['string'] - 1)
#         agg_df.drop('rating', axis=1, inplace=True)

#         if len(agg_df) != 0:
#                 agg_df.loc[:, "File Name"] = filename
#                 agg_df = (agg_df.head(1)
#                             .drop(['string','final rating'],axis=1)
#                             .set_index('File Name'))

#         return agg_df

#     elif len(df) == 1:
#         agg_df = df.copy()
#         agg_df.loc[:, "File Name"] = filename
#         agg_df = (agg_df.head(1)
#                             .drop(['string','rating'],axis=1)
#                             .set_index('File Name'))
#         return agg_df

#     else:
#         return None     
        

# # --------------Main Loop-------------- #
# startTime = datetime.now()
# f = open('log.md', 'wb')

# # set your working directory
# directory = 'd:/git/Invoice-Receipt-OCR/'
# dir_test_img = directory + 'test_image/'

# # reference for pdfminer looping. This matters a lot!
# argu = [(2, 0.5, 0.5), (5, 0.5, 0.5), (5, 0.5, 5), (100, 1, 5), (5, 1.5, 1.5)]
# argu2 = ['1', '3', '6']


# # main loop
# def main_loop(pdf_process=True, ocr_process=True):
#     csv = pd.DataFrame()
#     for filename in os.listdir(dir_test_img):
#         dir_file = "".join([dir_test_img, filename])
#         f.write('Analysing pdf {}...\n'.format(filename).encode('utf8'))

#         # If it's a pdf file, then...
#         if filename.endswith(".pdf"):
#             if pdf_process:
#                 # **************************************pdfminer process starts
#                 counter = 1
#                 id_df = pd.DataFrame()
#                 amount_df = pd.DataFrame()

#                 # Perform PDF Miner process:
#                 # Looping three times with different settings
#                 for i, j, k in argu:

#                     txt = pdf.convert_pdf(dir_file, char_margin=i, line_margin=j, boxes_flow=k)
#                     id_tem, amount_tem = regex_extraction(txt, "PDF Miner option {}".format(counter))

#                     # Append all DataFrames together
#                     id_df = id_df.append(id_tem)
#                     amount_df = amount_df.append(amount_tem)

#                     counter += 1
#                 # **************************************pdfminer process ends

#             if ocr_process:
#                 # **************************************ocr process starts
#                 counter = 1
#                 for i in argu2:

#                     txt = ocr.ocr_process(dir_file, page_seg_method=i)
#                     id_tem, amount_tem = regex_extraction(txt, "OCR process {}".format(counter))

#                     # Append all DataFrames from the above processes together
#                     id_df = id_df.append(id_tem)
#                     amount_df = amount_df.append(amount_tem)

#                     counter += 1
#                 # **************************************ocr process ends

#             # aggregate ratings based on amount
#             # do some ajustment on ratings
#             # print final aggregated rating
#             id_agg = agg_dfs(id_df, 'ID', filename)
#             amount_agg = agg_dfs(amount_df, 'Amount', filename)

#             if id_agg is not None or amount_agg is not None:
#                 agg_df = pd.concat([id_agg, amount_agg], axis=1)
#                 agg_df = agg_df.loc[:,['Amount','ID']]
#                 csv = csv.append(agg_df)          

#         else:
#                 # if it's not a pdf file, we do nothing... currently
#             pass

#     csv.to_csv("csv_result.csv")

#     print(datetime.now() - startTime)
#     # --------------Main Loop-------------- #


# if __name__ == "__main__":
#     main_loop(ocr_process=False)
