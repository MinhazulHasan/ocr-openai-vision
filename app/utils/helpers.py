import base64
import re
import pandas as pd
from typing import List


def encode_image(file):
    return base64.b64encode(file).decode('utf-8')


def load_data(file_path: str) -> pd.DataFrame:
    return pd.read_csv(file_path)


def format_wer(wer: float) -> str:
    return f"{wer*100:.3f}%"
