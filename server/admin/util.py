from datetime import datetime
import psycopg2
import re
import time
from functools import wraps

from flask import g, request, redirect, url_for


def save_written_post(data):
    """
    Save pre-validated data from WriteForm to db
    """
    title = data.get('postTitle')
    author = 'gautam'
    date = data.get('postDate')
    body = data.get('postBody')

    # Construct post slug
    slug = re.sub(' +', '-', title)
    slug = re.sub('[^0-9a-zA-z-]+', '', slug)
    slug = slug.lower()

    paragraphs = []
    graphs = body.split('\r\n')
    # Escape single quotes
    graphs = [graph.replace("'", "''") for graph in graphs if graph]

    conn = psycopg2.connect('postgresql:///profil_db')
    cursor = conn.cursor()

    # Write Post metadata
    meta_query = """
        insert into post_meta (title, author, post_date, post_slug) values
        ('{0}', '{1}', '{2}', '{3}');
    """.format(title, author, date, slug)
    cursor.execute(meta_query)
    
    # Get post_id of new post metadata
    new_post_id_query = """
      select post_id from post_meta where title='{0}' and post_date='{1}';
    """.format(title, date)
    cursor.execute(new_post_id_query)
    time.sleep(1)
    post_id_result = cursor.fetchall()

    # If duplicates, return failure
    if len(post_id_result) > 1:
        conn.rollback()
        return False, "Duplicate post metadata"
    post_id = post_id_result[0][0]

    # Write paragraphs to post_paragraph
    try:
        for graph in graphs:
            cursor.execute("""
                insert into post_paragraph(post_id, para_text) values
                ('{0}', '{1}');
            """.format(post_id, graph)
            )
    except Exception as e:
        conn.rollback()
        conn.close()
        return False, "Paragraphs failed to write"

    conn.commit()
    conn.close()
    return True, "SUCCESS"


def insert_links(graphs):
    """
    reintroduce html to links in post paragraphs
    """
    paragraphs = []
    for graph_data in graphs:
        graph = graph_data.get('paraText', '')
        start, occurences = re.subn(r'~~~', r'<a target="_blank" href="', graph)
        middle, occurences = re.subn(r'@@@', r'">', start)
        end, occurences = re.subn(r'%%%', r'</a>', middle)
        paragraphs.append({
            'paraId': graph_data.get('paraId'),
            'paraText': end
        })

    return paragraphs


def get_post_content(slug):
    """
    get post data from db
    """
    conn = psycopg2.connect('postgresql:///profil_db')
    cursor = conn.cursor()

    cursor.execute(get_post_meta_query(slug=slug))
    meta_data = cursor.fetchall()

    post_id = meta_data[0][0]
    title = meta_data[0][1]
    author = meta_data[0][2]
    post_date = datetime.strftime(meta_data[0][3], '%B %e, %Y')

    conn.close()
    graphs = get_paragraph_data(post_id)
    prev_slug, next_slug = get_prev_and_next_slugs(post_id)
    return {
        "title": title,
        "slug": slug,
        "author": author,
        "postDate": post_date,
        "paragraphs": graphs,
        "prevSlug": prev_slug,
        "nextSlug": next_slug
    }


def get_latest_post():
    """
    get most recent blog post data
    """
    conn = psycopg2.connect('postgresql:///profil_db')
    cursor = conn.cursor()

    latest_post_query = """
        select post_id, title, author, post_date, post_slug from post_meta order by post_date DESC limit 1
    """
    cursor.execute(latest_post_query)
    meta_data = cursor.fetchall()
    post_id = meta_data[0][0]
    title = meta_data[0][1]
    slug = meta_data[0][4]
    author = meta_data[0][2]
    post_date = datetime.strftime(meta_data[0][3], '%B %e, %Y')

    conn.close()
    graphs = get_paragraph_data(post_id)
    prev_slug, next_slug = get_prev_and_next_slugs(post_id)
    return {
        "title": title,
        "slug": slug,
        "author": author,
        "postDate": post_date,
        "paragraphs": graphs,
        "prevSlug": prev_slug,
        "nextSlug": next_slug
    }


def get_post_meta_query(slug=None, post_id=None):
    """
    get post meta data based on either slug or post_id
    """
    if not slug and not post_id:
        return None

    if slug:
        return """
            select post_id, title, author, post_date, post_slug from post_meta where post_slug = '{0}'
        """.format(slug)
    else:
        return """
            select post_id, title, author, post_date, post_slug from post_meta where post_id = {0}
        """.format(post_id)


def get_paragraph_data(post_id):
    """
    get paragraph data for post_id
    """
    conn = psycopg2.connect('postgresql:///profil_db')
    cursor = conn.cursor()

    paragraph_query = """
        select para_id, para_text from post_paragraph where post_id = {0} order by para_id
    """.format(post_id)
    cursor.execute(paragraph_query)
    paragraph_data = cursor.fetchall()

    conn.close()
    # convert links to markup
    return insert_links([{
        'paraId': graph_data[0], 'paraText': graph_data[1]
            } for graph_data in paragraph_data])


def get_prev_and_next_slugs(post_id):
    """
    get previous and next slugs
    """
    conn = psycopg2.connect('postgresql:///profil_db')
    cursor = conn.cursor()

    lag_lead_query = """
        select post_id, lag(post_slug, 1) over (order by post_date), lead(post_slug, 1) over (order by post_date) from post_meta;
    """
    cursor.execute(lag_lead_query)
    lag_lead_data = cursor.fetchall()

    conn.close()
    return [(slugs[1], slugs[2]) for slugs in lag_lead_data if slugs[0] == post_id][0]


def get_pre_login_info(username):
    conn = psycopg2.connect('postgresql:///profil_db')
    cursor = conn.cursor()

    pre_login_query = """
        select nacl, passhash from users where username='{0}'
    """.format(username)

    cursor.execute(pre_login_query)
    pre_login_data = cursor.fetchall()
    conn.close()

    if pre_login_data:
        return pre_login_data[0][0], pre_login_data[0][1]
    else:
        return None, None
