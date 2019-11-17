import json
import re
from collections import namedtuple

import psycopg2

from admin.util import interpret_editor_content

SearchResult = namedtuple('SearchResult', ('term post_slug text post_title '
                                           'para_id before after'))


def search_post_data(terms):
    """
    Search title and post paragraphs for the search terms
    """
    title_query = """
    select '{0}', pm.post_slug, pm.title, pm.title, -1, '', ''
    from post_meta pm
    where to_tsvector(pm.title) @@ to_tsquery('{1}')
    """

    para_query = """
    select search_term, post_slug, text, post_title, para_id, before, after
    from (
        select
            '{0}' as search_term,
            pm.post_slug as post_slug,
            pp.para_text as text,
            pm.title as post_title,
            pp.para_id as para_id,
            lag(pp.para_text, 1) over (order by pp.para_id) as before,
            lead(pp.para_text, 1) over (order by pp.para_id) as after
        from post_meta pm
        join post_paragraph pp
        on pp.post_id=pm.post_id
    ) a
    where to_tsvector(text) @@ to_tsquery('{1}')
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

    all_results = []
    for source, query in (('title', title_query), ('paragraphs', para_query)):
        cursor.execute(query)
        result_data = cursor.fetchall()
        initial_results = [
            SearchResult(
                term=result[0],
                post_slug=result[1],
                text=result[2],
                post_title=result[3],
                para_id=result[4],
                before=result[5],
                after=result[6]
            ) for result in result_data
        ]
        paragraph_results = []
        if source == 'paragraphs':
            for result in initial_results:
                interpreted = []
                for text in (
                        result.before, result.text, result.after):
                    loaded = json.loads(text)
                    if not loaded:
                        loaded = {}
                    interpreted.append(
                        interpret_editor_content(
                            [(0, {'insert': loaded.get('insert')})]))
                paragraph_results.append(
                    SearchResult(
                        term=result.term,
                        post_slug=result.post_slug,
                        text=' '.join(text[0].get('paraText') for text in interpreted),
                        post_title=result.post_title,
                        para_id=result.para_id,
                        before=result.before,
                        after=result.after
                    )
                )
        if not paragraph_results:
            all_results += initial_results
        else:
            all_results += paragraph_results
    return parse_results_for_highlights(all_results)


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
    return {'results': for_display}
