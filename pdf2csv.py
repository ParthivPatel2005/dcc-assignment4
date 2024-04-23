import fitz
import pandas as pd
import csv

def pdf_to_csv(filename):
    Document =fitz.open(filename)
    n = Document.page_count

    df = pd.DataFrame()
    for i in range(0,n):
        page = Document[i]
        table = page.find_tables()
        df = pd.concat([ df, table[0].to_pandas()])

    df.to_csv('file2.csv', index=False)

pdf_to_csv(r"flask_tutorial\fLdxwIUYK5.pdf")
pdf_to_csv(r"flask_tutorial\VyOSptiM8I.pdf")

