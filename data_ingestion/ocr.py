import pdfplumber
from typing import Sequence
from datetime import datetime
from data_models.transaction import OcrTransactionRaw


def ReadDigitalPdf(file_path) -> Sequence[OcrTransactionRaw]:
    ocr_transactions = []

    with pdfplumber.open(file_path) as pdf:
        for page_idx, page in enumerate(pdf.pages, start=1):
            tables = page.extract_tables(
                {
                    "vertical_strategy": "lines",
                    "horizontal_strategy": "lines",
                    "explicit_vertical_lines": [page.width * 0.05, page.width * 0.95],
                    "snap_x_tolerance": 9,
                }
            )
            print(tables)
            print(len(tables))
            for tab_idx, tab in enumerate(tables, start=1):
                for row_idx, row in enumerate(tab, start=1):
                    try:
                        print(f"tab: {tab_idx}, row: {row_idx}")
                        tx = OcrTransactionRaw(
                            filename=file_path,
                            page=page_idx,
                            tab=tab_idx,
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
