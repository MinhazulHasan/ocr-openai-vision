
def get_prompt_template():
    PROMPT_TEMPLATE = f"""
        Analyze the image and do OCR of the HANDWRITTEN PART to extract text from the image.
        YOU ARE BOUND TO RESPONSE JUST THE HANDWRITTEN TEXT FROM THE IMAGE. DO NOT ADD ANYTHING ELSE.
    """
    return PROMPT_TEMPLATE
