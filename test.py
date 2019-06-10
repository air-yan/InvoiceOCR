import pdf
import ocr
import extract_amount

test_regex = ['Total Amount',
              '(?<!Tax )(?<!Sub)(?<!Sub )(Total[^0-9]{1,30}[0-9,]*\.\d\d)']

test_regex2 = [
    'Balance', '(?<!Previous )(?<!Prior )(?<!Ending )(?<!Past Due )(Balance[^0-9]{1,30}[0-9,]*\.\d\d)']

test_regex3 = ['Amount Due', '(Amount Due[^0-9]{1,30}[0-9,]*\.\d\d)']

file = r'US invoice/731_1722485_usd_20190228_invoice_553369247008.pdf'

# ---------------pdf minder-------------- #
# argu = [(2, 0.5, 0.5), (5, 0.5, 0.5), (5, 0.5, 5), (100, 1, 5), (5, 1.5, 1.5)]

# counter = 1
# for i, j, k in argu:
#     txt = pdf.convert_pdf(file,
#         char_margin=i, line_margin=j, boxes_flow=k)

#     result = extract_amount.regex_parsser(
#         txt, test_regex, 'Total Amount', extract_amount.dic)
    # print(counter)
    # print(result)
    # print('\n')
# ---------------pdf minder-------------- #



txt = ocr.ocr_process(file)

result = extract_amount.amount_parsser(
        txt, test_regex, 'Total Amount', extract_amount.dic)

print(result)


