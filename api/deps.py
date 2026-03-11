import pandas as pd
import tempfile


def save_uploaded_csv(file) -> str:
    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".csv")
    tmp.write(file.file.read())
    tmp.close()
    return tmp.name
