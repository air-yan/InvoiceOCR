import pdf
import extract_amount
import extract_id
import main

filename = 'test_image/CSCINV20190125_7766149_81107743398.pdf'

def test(filename,i,j,k):
    txt = pdf.convert_pdf(filename,char_margin=i, line_margin=j, boxes_flow=k)
    df1, df2 = main.regex_extraction(txt,'test')
    print(df1)
    print(df2)
    
argu = [(2, 0.5, 0.5), (5, 0.5, 0.5), (5, 0.5, 5), (100, 1, 5), (5, 1.5, 1.5)]
usethis = argu[3]

txt = pdf.convert_pdf(filename,char_margin=usethis[0], line_margin=usethis[1], boxes_flow=usethis[2])
df1, df2 = main.regex_extraction(txt,'test')

# test('test_image/731_1722485_usd_20190228_invoice_553369247008.pdf',2, 0.5, 0.5)

print(df1)