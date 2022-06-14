import re, csv
from os import listdir, environ
from PyPDF2 import PdfFileReader

debug = environ.get("DEBUG", 0)
fields = ["Date", "Numéro CHQ", "Montant"]
data = []

# Open PDFs and scan for wanted data
for pdf in listdir("./input"):
    # Prepare PDF Object for reading
    pdfObj = open("./input/" + pdf, "rb")
    preRead = PdfFileReader(pdfObj, strict=False)
    if preRead.isEncrypted:
        preRead.decrypt('')
    pageObj = preRead.getPage(0)
    read = pageObj.extract_text()

    regOpposition = re.compile(r'OPPOSITION SUR CHEQUE\(S\)')
    opposition = regOpposition.search(read)
    regEcheance = re.compile(r'ECHEANCE')
    echeance = regEcheance.search(read)

    # Match only wanted PDFs
    if opposition and not echeance:
        sep=";"
        regDate = re.compile(r'[0-9]{1,2}/.+/[0-9]{4}')
        date = sep.join(regDate.findall(read))
        regSum = re.compile(r'[0-9]+,[0-9]{2}')
        sum = sep.join(regSum.findall(read))
        regCheck = re.compile(r'numéro[0-9]{7}')
        check = regCheck.search(read).group(0).replace("numéro", "")

        # Prepare data for CSV export
        row = [ date, check, sum ]
        data.append(row)

        if debug:
            print(row)
    else:
        continue

if not debug:
    with open("Oppositions.csv", 'w') as exportCsv:
        writer = csv.writer(exportCsv)
        writer.writerow(fields)
        writer.writerows(data)
else:
    print(data)