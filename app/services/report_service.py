import os
from app.services.ocr_service import get_ocr
from app.utils.helpers import encode_image
from app.utils.logger import report_logger
import pandas as pd
from app.utils.helpers import format_wer
from app.utils.text_processing import calculate_word_error_rate


def _bulk_ocr():
    test_data_path = "test-data"
    report_data_path = os.path.join("report", "report.csv")
    data = []

    for file_name in os.listdir(test_data_path):
        if file_name.endswith(".jpg") or file_name.endswith(".jpeg") or file_name.endswith(".png"):
            image_name = file_name.split(".")[0]
            image_path = os.path.join(test_data_path, file_name)

            with open(image_path, "rb") as f:
                file_content = f.read()
                base64_image = encode_image(file_content)
                response = get_ocr(base64_image)
                data.append({"Image Name": image_name, "OpenAI Response": response})
                report_logger.info(f"\nOCR response for {file_name}: {response}\n\n\n")

    df = pd.DataFrame(data)
    df.to_csv(report_data_path, index=False)
    report_logger.info("\n\n\nBulk OCR completed\n\n")



def analyze_ocr_results(df: pd.DataFrame) -> dict:
    df['WER'] = df.apply(lambda row: calculate_word_error_rate(row['Actual Response'], row['OpenAI Response']), axis=1)
    df['WER_formatted'] = df['WER'].apply(format_wer)
    
    results = {
        'average_wer': format_wer(df['WER'].mean()),
        'wer_by_image': df[['Image Name', 'WER_formatted']].rename(columns={'WER_formatted': 'WER'}).to_dict('records'),
        'total_images': len(df),
        'perfect_matches': sum(df['WER'] == 0),
    }
    
    return results, df