import matplotlib.pyplot as plt
import io
import base64
import pandas as pd


def create_bar_chart(df: pd.DataFrame) -> str:
    plt.figure(figsize=(12, 6))
    plt.bar(df['Image Name'], df['WER'] * 100)
    plt.title('Word Error Rate by Image')
    plt.xlabel('Image Name')
    plt.ylabel('Word Error Rate (%)')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    
    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    return base64.b64encode(img.getvalue()).decode()


def create_pie_chart(average_wer: float) -> str:
    plt.figure(figsize=(8, 8))
    plt.pie([100 - average_wer, average_wer], 
            labels=['Total', 'WER'], 
            autopct='%1.1f%%', 
            startangle=90)
    plt.title('Proportion of WRE')
    
    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    return base64.b64encode(img.getvalue()).decode()