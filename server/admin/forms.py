from datetime import datetime
import json

from util import parse_simple_fields


def validate_write_post_form(data):
    """
    Validate WriteForm react component
    """
    title = parse_simple_fields(data.get('postTitle'))
    if not title:
        return False, "no post title"

    date = parse_simple_fields(data.get('postDate'))
    try:
        datetime.strptime(date, '%Y-%m-%d')
    except Exception as e:
        return False, e.message

    body = data.get('postBody')
    if not body:
        return False, "no post body"

    return True, "SUCCESS"
