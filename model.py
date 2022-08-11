def predict_bookmark(one_page_text: str, threshold: int = 50):
    text_len = len(one_page_text)

    if text_len > threshold:
        formtype = '1065'
        formpage = '0'
    else:
        formtype = 'CA 565'
        formpage = '2'
    
    return {
        'formtype': formtype,
        'formpage': formpage
    }