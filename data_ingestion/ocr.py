import pdfplumber
from datetime import datetime
from data_models.transaction import OcrTransactionRaw


def ReadDigitalPdf(file_path):
    ocr_transactions = []

    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            tables = page.extract_tables(
                {
                    "vertical_strategy": "lines",
                    "horizontal_strategy": "lines",
                    "explicit_vertical_lines": [page.width * 0.05, page.width * 0.95],
                    "snap_x_tolerance": 9,
                }
            )
            for tab in tables:
                for row_idx, row in enumerate(tab, start=1):
                    # if row.count(None) + row.count('') >= len(row) - 2 or isinstance(row[1][0], ):
                    #    continue  # ignora righe quasi vuote

                    # row_dict = dict(zip(headers, row))
                    print(row)
                    amount = 0
                    c = -1

                    try:
                        for amt in (row[3], row[4]):
                            if (amt is not None) and (amt != ""):
                                if "," in amt:
                                    amt = amt.replace(".", "").replace(",", ".")
                                amount += c * float(amt)
                            c *= -1
                        tx = OcrTransactionRaw(
                            filename=file_path,
                            row=row_idx,
                            booking_dt=datetime.strptime(row[0], "%d/%m/%Y").date(),
                            value_dt=datetime.strptime(row[1], "%d/%m/%Y").date(),
                            amount=amount,
                            description=row[2].strip() if row[2] else None,
                        )
                        ocr_transactions.append(tx)
                    except Exception as e:
                        print(f"Errore nel parsing della riga {row_idx}: {e}")
    return ocr_transactions
