from datetime import datetime
import json
import psycopg2
import re
import time
from datetime import datetime

import psycopg2

ATT_TAGS = {
    'link': ('<a href="{}" target="_blank">', '</a>'),
    'italic': ('<i>', '</i>'),
    'bold': ('<b>', '</b>'),
    'underline': ('<u>', '</u>')
}

def parse_simple_fields(json_data):
    """
    Parses form inputs from plain text editor fields, no expected formatting
    """
    loaded = json.loads(json_data)
    data = []
    if len(loaded) > 0:
        for item in loaded:
            data.append(item.pop('insert').strip('\n'))
    if len(data) == 1:
        return data[0]
    return data


def parse_long_form_fields(json_data):
    """
    Parses form inputs from formatted editor fields, assuming multiple formatted fields
    """
    loaded = json.loads(json_data)
    graphs = [json.dumps(graph) for graph in loaded]
    return graphs


def save_written_post(data):
    """
    Save pre-validated data from WriteForm to db
    """
    title = parse_simple_fields(data.get('postTitle'))
    author = 'gautam'
    date = parse_simple_fields(data.get('postDate'))
    graphs = parse_long_form_fields(data.get('postBody'))

    # Construct post slug
    slug = re.sub(' +', '-', title)
    slug = re.sub('[^0-9a-zA-z-]+', '', slug)
    slug = slug.lower()

    conn = psycopg2.connect('postgresql:///profil_db')
    cursor = conn.cursor()

    # Write Post metadata
    meta_query = """
        insert into post_meta (title, author, post_date, post_slug)
        values ('{0}', '{1}', '{2}', '{3}');
    """.format(title, author, date, slug)
    cursor.execute(meta_query)

    # Get post_id of new post metadata
    new_post_id_query = """
      select post_id
      from post_meta
      where title='{0}'
      and post_date='{1}';
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
                insert into post_paragraph(post_id, para_text)
                values ('{0}', '{1}');
            """.format(post_id, graph)
            )
    except Exception as e:
        conn.rollback()
        conn.close()
        return False, "Paragraphs failed to write {}".format(e)

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
        start, occurences = re.subn(r'~~~', r'<a target="_blank" href="',
                                    graph)
        middle, occurences = re.subn(r'@@@', r'">', start)
        end, occurences = re.subn(r'%%%', r'</a>', middle)
        paragraphs.append({
            'paraId': graph_data.get('paraId'),
            'paraText': end
        })

    return paragraphs


def interpret_editor_content(para_list):
    """
    Formats HTML for limited set of attributes from long form content
     from the GUI editor
    """
    paragraphs = []
    for para in para_list:
        text = para[1].get('insert')
        attributes = para[1].get('attributes')
        if attributes:
            for att, att_data in attributes.items():
                html_open = ATT_TAGS[att][0]
                if att == 'link':
                    html_open = html_open.format(att_data)
                text = html_open + text + ATT_TAGS[att][1]
        paragraphs.append({
            'paraId': para[0],
            'paraText': text
            })
    return paragraphs


def get_post_content(slug):
    """
    Get post data from db for a particular slug
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
    Get most recent blog post data by post date
    """
    conn = psycopg2.connect('postgresql:///profil_db')
    cursor = conn.cursor()

    latest_post_query = """
        select post_id, title, author, post_date, post_slug
        from post_meta
        order by post_date DESC
        limit 1
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
    Get post meta data based on either slug or post_id
    """
    if not slug and not post_id:
        return None

    if slug:
        return """
            select 
                post_id,
                title,
                author,
                post_date,
                post_slug
            from post_meta
            where post_slug = '{0}'
        """.format(slug)
    else:
        return """
            select
                post_id,
                title,
                author,
                post_date,
                post_slug
            from post_meta
            where post_id = {0}
        """.format(post_id)


def get_paragraph_data(post_id):
    """
    Get HTML formatted paragraph data for post_id
    """
    conn = psycopg2.connect('postgresql:///profil_db')
    cursor = conn.cursor()

    paragraph_query = """
        select para_id, para_text
        from post_paragraph
        where post_id = {0}
        order by para_id
    """.format(post_id)
    cursor.execute(paragraph_query)
    paragraph_data = cursor.fetchall()

    conn.close()
    graphs = [{
        'paraId': graph_data[0],
        'paraText': graph_data[1]
    } for graph_data in paragraph_data]

    # try parsing json paragraph data first
    try:
        return interpret_editor_content([(
            graph.get('paraId'), json.loads(graph.get('paraText'))
        ) for graph in graphs])
    except Exception as e:
        # expected failure case for early posts, pre-editor
        pass
    # convert links to markup for early pre-editor posts
    return insert_links(graphs)


def get_prev_and_next_slugs(post_id):
    """
    Get previous and next slugs for a given post_id
    """
    conn = psycopg2.connect('postgresql:///profil_db')
    cursor = conn.cursor()

    lag_lead_query = """
        select
            post_id,
            lag(post_slug, 1) over (order by post_date),
            lead(post_slug, 1) over (order by post_date)
        from post_meta;
    """
    cursor.execute(lag_lead_query)
    lag_lead_data = cursor.fetchall()

    conn.close()
    return [(slugs[1], slugs[2]) for slugs in lag_lead_data
            if slugs[0] == post_id][0]


def get_pre_login_info(username):
    """
    Get auth related info for a given username
    """
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
