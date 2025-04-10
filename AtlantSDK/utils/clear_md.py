import re


def clean_text(text: str):
    """
    Markdown text cleanup function
    Args:
        text (str): A markdown text

    Returns:
        str: Cleared text.
    """

    cleaned_text = re.sub(r'\*\*(.*?)\*\*', r'\1', text)

    cleaned_text = re.sub(r'\*(.*?)\*', r'\1', cleaned_text)

    cleaned_text = re.sub(r'(.*?)', r'\1', cleaned_text)

    cleaned_text = re.sub(r'~~(.*?)~~', r'\1', cleaned_text)
    cleaned_text = re.sub(r'###',"", cleaned_text)
    cleaned_text = cleaned_text.replace("`", "")

    return cleaned_text