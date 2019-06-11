import copy
import pandas as pd
from ocr import ocr_process
from extract_amount import amount_parsser, dic

# 路径与ocr
file_path = r'US invoice/invoice_FS40177.pdf'
ocr_result = ocr_process(file_path) # 这一步会花较长时间

# 准备regex
totalAmountRegex = {'name': 'Total Amount',
                     'regex': '(?<!Tax )(?<!Sub)(?<!Sub )(Total[^0-9]{1,30}[0-9,]*\.\d\d)'}
balanceAmountRegex = {'name': 'Balance',
                       'regex': '(?<!Previous )(?<!Prior )(?<!Ending )(?<!Past Due )(Balance[^0-9]{1,30}[0-9,]*\.\d\d)'}
dueAmountRegex = {'name': 'Amount Due',
                   'regex': '(Amount Due[^0-9]{1,30}[0-9,]*\.\d\d)'}

# 用deepcopy防止pass by reference
result_dic = amount_parsser(ocr_result, totalAmountRegex, dic)
result_dic1 = amount_parsser(ocr_result, balanceAmountRegex, copy.deepcopy(result_dic))
result_dic2 = amount_parsser(ocr_result, dueAmountRegex, copy.deepcopy(result_dic1))

# print 每一步的结果
print('-'*10 + 'Show each steps' + '-'*10)
print(result_dic)
print(result_dic1)
print(result_dic2)
print('-'*10 + 'Show each steps' + '-'*10 + '\n')

# print 所有结果
print('-'*10 + 'Show All Results' + '-'*10)
print(pd.DataFrame(result_dic2))
print('-'*10 + 'Show All Results' + '-'*10 + '\n')


# 选第一个得分最高的
best_index = result_dic2['score'].index(max(result_dic2['score']))
best_df = pd.DataFrame(result_dic2).iloc[best_index,:]
print('-'*10 + 'Best result' + '-'*10)
print(best_df)
print('-'*10 + 'Best result' + '-'*10 + '\n')