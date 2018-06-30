
from datetime import datetime

def validate_write_post_form(data):
    """
    Validate WriteForm react component
    """
    title = data.get('postTitle')
    if not title:
        return False, "no post title"

    date = data.get('postDate')
    try:
        datetime.strptime(date, '%Y-%m-%d')
    except Exception as e:
        return False, e

    body = data.get('postBody')
    if not body:
        return False, "no post body"

    return True, "SUCCESS"