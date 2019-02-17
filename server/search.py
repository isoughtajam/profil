import re
from collections import namedtuple

import psycopg2

SearchResult = namedtuple('SearchResult', 'term post_slug text post_title')


def search_post_data(terms):
    """
    Search title and post paragraphs for the search terms
    """
    title_query = """
    select '{0}', pm.post_slug, pm.title, pm.title
    from post_meta pm
    where to_tsvector(pm.title) @@ to_tsquery('{1}')
    """

    para_query = """
    select '{0}', pm.post_slug, pp.para_text, pm.title
    from post_meta pm
    join post_paragraph pp on pp.post_id=pm.post_id
    where to_tsvector(pp.para_text) @@ to_tsquery('{1}')
    """
    conn = psycopg2.connect('postgresql:///profil_db')
    cursor = conn.cursor()

    title_union = [
        title_query.format(term.replace('& ', '').replace('*', ''), term)
        for term in terms
    ]
    para_union = [
        para_query.format(term.replace('& ', '').replace('*', ''), term)
        for term in terms
    ]
    title_query = ' union all '.join(title_union)
    para_query = ' union all '.join(para_union)
    search_query = ' union all '.join([title_query, para_query])

    cursor.execute(search_query)
    result_data = cursor.fetchall()
    results = [
        SearchResult(
            term=result[0],
            post_slug=result[1],
            text=result[2],
            post_title=result[3]) for result in result_data
    ]
    # import pdb
    # pdb.set_trace()
    return parse_results_for_highlights(results)


def parse_search_terms_into_tsquery(term_string):
    """
    Turn url encoded string from search request into postgres tsquery strings
    """
    # Strip pluses, url encoded commas, single quotes from beginning and
    # end of search string
    term_str = term_string.strip(',').strip(' ').replace('%27', '\'')

    # Split on url encoded commas into search terms and remove comma terms
    splits = re.split(',', term_str)
    splits = [split for split in splits if split != ',']

    # Strip pluses from beginning and end of terms
    splits = [split.strip(' ') for split in splits]

    # Replace pluses within terms with ampersand
    splits = [split.replace(' ', ' & ') for split in splits]

    return splits


def parse_results_for_highlights(result_data):
    """
    Put <span> tags around searched text in resulting title or paragraph for
     visual highlighting

    For title matches only include title in final result text. For paragraph
     matches include 10 words on either side of match for context.

    Final payload should be [(slug, final text)]
    """
    for_display = []
    index = 0
    for result in result_data:
        # if match is in URL, disregard match
        result_text = result.text
        result_text = re.sub(r'(?<=~~~)[a-zA-Z://.0-9_-]+', '', result_text)
        result_text = re.sub(r'[~@%]', '', result_text)
        if not re.search(result.term, result_text, re.IGNORECASE):
            continue

        # Split text on term in order to add span tags
        regex = "(" + result.term + ")(?i)"
        splits = re.split(regex, result_text)
        amended = []
        for split in splits:
            if split.lower() == result.term:
                amended.append("<a href='/blog/{}/'>".format(result.post_slug)
                               + split + "</a>")
            else:
                amended.append(split)
        for_display.append({
            'id': index,
            'slug': result.post_slug,
            'search_result': ''.join(amended),
            'post_title': result.post_title
        })
        index += 1

    # import pdb
    # pdb.set_trace()
    return {'results': for_display}
