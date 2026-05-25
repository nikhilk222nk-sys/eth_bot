import csv
import os
from datetime import datetime


class TradeLogger:

    FILE_NAME = "trade_history.csv"

    @staticmethod
    def log_signal(
        signal,
        price,
        confidence,
        imbalance,
        delta,
        btc_trend,
        higher_tf,
        sweep
    ):

        file_exists = os.path.isfile(
            TradeLogger.FILE_NAME
        )

        with open(
            TradeLogger.FILE_NAME,
            mode='a',
            newline=''
        ) as file:

            writer = csv.writer(file)

            # HEADER
            if not file_exists:

                writer.writerow([
                    "timestamp",
                    "signal",
                    "price",
                    "confidence",
                    "imbalance",
                    "delta",
                    "btc_trend",
                    "higher_tf",
                    "sweep"
                ])

            # DATA
            writer.writerow([
                datetime.utcnow(),
                signal,
                price,
                confidence,
                imbalance,
                delta,
                btc_trend,
                higher_tf,
                sweep
            ])

        print("Signal Logged")