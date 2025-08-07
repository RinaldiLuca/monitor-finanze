import pdfplumber
from datetime import datetime
from data_models.transaction import OcrTransactionRaw


def ReadDigitalPdf(file_path) -> list[OcrTransactionRaw]:
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
                    try:
                        tx = OcrTransactionRaw(
                            filename=file_path,
                            row=row_idx,
                            booking_dt=row[0],
                            value_dt=row[1],
                            amount=row[4],
                            negative_amount=row[3],
                            description=row[2],
                        )
                        ocr_transactions.append(tx)
                    except Exception as e:
                        print(f"Errore nel parsing della riga {row_idx}: {e}")
    return ocr_transactions
