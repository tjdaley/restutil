"""
codesearch.py - Search codified laws

Copyright (c) by Thomas J. Daley, J.D.
"""
import util.functions as FN
from whoosh.index import open_dir
from whoosh.qparser import MultifieldParser, FuzzyTermPlugin
from collections import namedtuple


SearchResult = namedtuple(
    'SearchResult',
    'code, code_name, title, subtitle, chapter, subchapter, section_number, section_name, text, future_effective_date, highlights'
)


class CodeSearch(object):
    @staticmethod
    def search(query_text, code_list):
        """
        Search codified laws, returning the results.

        Args:
            query (str): Query string entered by user.
        Returns:
            (list): List of SearchResult tuples
        """
        parser = MultifieldParser(['section_name', 'text', 'section_number'], schema=FN.schema())
        parser.add_plugin(FuzzyTermPlugin())
        index = open_dir(FN.INDEX_PATH, FN.index_name(None))

        # create code clause if user is narrowing the query to a subset of all
        # indexed codes.
        if code_list != '*' and code_list != '':
            codes = code_list.upper().split(' ')
            code_clauses = [f'code:{c} ' for c in codes]
            code_clause = ' OR '.join(code_clauses)
            query_text = query_text + ' ' + code_clause

        # Convert query string to query-language query
        query = parser.parse(query_text)

        # Search for results
        documents = []
        with index.searcher() as searcher:
            result = searcher.search(query)
            result.fragmenter.charlimit = None
            result.fragmenter.maxchars = 1000
            result.fragmenter.surround = 50
            for doc in result:
                documents.append(SearchResult(
                    doc.get('code', "NO CODE"),
                    doc.get('code_name', "NO CODE NAME"),
                    doc.get('title', "NO TITLE"),
                    doc.get('subtitle', "NO SUBTITLE"),
                    doc.get('chapter', "NO CHAPTER"),
                    doc.get('subchapter', "NO SUBCHAPTER"),
                    doc.get('section_number', "NO SECTION NUMBER"),
                    doc.get('section_name', "NO SECTION NAME"),
                    doc.get('text', "NO TEXT"),
                    doc.get('future_effective_date', "N/A"),
                    doc.highlights('text')
                ))
        return documents
