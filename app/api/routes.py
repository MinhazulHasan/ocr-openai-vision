from fastapi import APIRouter, UploadFile, File, HTTPException, BackgroundTasks
from app.services.ocr_service import get_ocr
from app.services.report_service import _bulk_ocr, analyze_ocr_results
from app.utils.visualization import create_bar_chart, create_pie_chart
from app.utils.helpers import encode_image, load_data
from app.utils.logger import report_logger
import pandas as pd
from fastapi.responses import HTMLResponse
import os
import pdfkit


router = APIRouter()

@router.post("/do_ocr/")
async def do_ocr(file: UploadFile = File(...)):
    if file.content_type not in ["image/jpg", "image/jpeg", "image/png"]:
        raise HTTPException(status_code=400, detail="Invalid file type. Only JPEG and PNG are supported.")
    
    file_content = await file.read()
    base64_image = encode_image(file_content)
    response = get_ocr(base64_image)
    report_logger.info(f"\nOCR response: {response}\n\n\n")
    return {"response": response}


@router.get("/bulk_ocr")
async def bulk_ocr(background_tasks: BackgroundTasks):
    report_logger.info("\n\n\nBulk OCR started\n\n")
    background_tasks.add_task(_bulk_ocr)
    return {"message": "Bulk OCR started"}


@router.post("/analyze_ocr")
async def analyze_ocr():
    try:
        df = load_data(os.path.join("report", "report.csv"))
        analysis, df = analyze_ocr_results(df)
        
        bar_chart = create_bar_chart(df)
        pie_chart = create_pie_chart(float(analysis['average_wer'].strip('%')))
        
        html_content = f"""
            <html>
                <head>
                    <title>OCR Analysis Results</title>
                    <style>
                        body {{ font-family: Arial, sans-serif; margin: 0; padding: 20px; }}
                        h1 {{ color: #333; }}
                        .chart {{ margin-bottom: 30px; }}
                        table {{ border-collapse: collapse; width: 100%; }}
                        th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
                        th {{ background-color: #f2f2f2; }}
                    </style>
                </head>
                <body>
                    <h1>OCR Analysis Results</h1>
                    <p>Average Word Error Rate: {analysis['average_wer']}</p>
                    <p>Total Images: {analysis['total_images']}</p>
                    <p>Perfect Matches: {analysis['perfect_matches']}</p>
                    
                    <div class="chart">
                        <h2>Word Error Rate by Image</h2>
                        <img src="data:image/png;base64,{bar_chart}" alt="Bar Chart of WER by Image">
                    </div>
                    
                    <div class="chart">
                        <h2>Proportion of Perfect Matches</h2>
                        <img src="data:image/png;base64,{pie_chart}" alt="Pie Chart of Perfect Matches">
                    </div>
                    
                    <h2>Word Error Rate by Image</h2>
                    <table>
                        <tr>
                            <th>Image Name</th>
                            <th>Word Error Rate</th>
                        </tr>
                        {"".join(f"<tr><td>{item['Image Name']}</td><td>{item['WER']}</td></tr>" for item in analysis['wer_by_image'])}
                    </table>
                </body>
            </html>
        """
            
        return analysis, HTMLResponse(content=html_content)
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))