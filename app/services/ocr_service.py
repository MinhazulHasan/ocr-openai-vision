import requests
from app.core.config import settings
from fastapi import HTTPException
from app.core.prompts import get_prompt_template

def get_ocr(base64_image):
    prompt_template = get_prompt_template()
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {settings.OPENAI_API_KEY}"
    }
    payload = {
        "model": settings.GPT_MODEL,
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": prompt_template
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                                "url": f"data:image/jpeg;base64,{base64_image}"
                            }
                    }
                ]
            }
        ],
        "max_tokens": 300
    }
    
    try:
        response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
        response.raise_for_status()
        response_json = response.json()
        content = response_json['choices'][0]['message']['content']
        return content
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=502, detail=f"Error communicating with OpenAI API: {e}")
    except KeyError:
        raise HTTPException(status_code=500, detail="Unexpected response format from OpenAI API")