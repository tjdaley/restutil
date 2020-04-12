"""
codesearch.py - Search codified laws

Copyright (c) by Thomas J. Daley, J.D.
"""
import glob
import os
import util.functions as FN
from whoosh.index import open_dir
from whoosh.qparser import MultifieldParser, FuzzyTermPlugin, QueryParser
from collections import namedtuple
import dotenv
import json

# Load environment variables
dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
dotenv.load_dotenv(dotenv_path)


class CodeSearch(object):
    @staticmethod
    def list_codes():
        """
        Retrieve a list of searchable codes.
        """
        code_path = os.environ.get('CODE_PATH')
        files = glob.glob(f'{code_path}/??.json')
        codes = []
        for code_file in files:
            with open(code_file, 'r') as fp:
                config = json.load(fp)
            code_name = config['code_name']
            if CodeSearch.is_searchable(code_name):
                searchable = 'Y'
            else:
                searchable = 'N'
            codes.append(
                {
                    'code': code_name,
                    'code_name': config['code_full_name'],
                    'version': '1.0.0',
                    'searchable': searchable
                }
            )
        return codes

    @staticmethod
    def is_searchable(code_name: str) -> bool:
        """
        Determine whether there is at least one article having
        the given code_name.

        Args:
            code_name (str): Two-letter code abbreviation.
        Returns:
            (bool): True if there is at least one article, otherwise False
        """
        parser = QueryParser('code', schema=FN.schema())
        query = parser.parse(code_name.lower())
        index = open_dir(FN.INDEX_PATH, FN.index_name(None))
        with index.searcher() as searcher:
            result = searcher.search(query, limit=1)
        return result.scored_length() > 0


    @staticmethod
    def search(query_text, code_list):
        """
        Search codified laws, returning the results.

        Args:
            query (str): Query string entered by user.
            code_list (str): Space-delimited list of codes to search or '*' or '' for ALL.
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
        print(code_clause)
        print(query_text)
        # Convert query string to query-language query
        query = parser.parse(query_text)
        print(query)

        # Search for results
        documents = []
        with index.searcher() as searcher:
            result = searcher.search(query, terms=True)
            result.fragmenter.charlimit = None
            result.fragmenter.maxchars = 1000
            result.fragmenter.surround = 50
            for doc in result:
                documents.append({
                    'code': doc.get('code', "NO CODE"),
                    'code_name': doc.get('code_name', "NO CODE NAME"),
                    'title': doc.get('title', "NO TITLE"),
                    'subtitle': doc.get('subtitle', "NO SUBTITLE"),
                    'chapter': doc.get('chapter', "NO CHAPTER"),
                    'subchapter': doc.get('subchapter', "NO SUBCHAPTER"),
                    'section_number': doc.get('section_number', "NO SECTION NUMBER"),
                    'section_name': doc.get('section_name', "NO SECTION NAME"),
                    'text': doc.get('text', "NO TEXT"),
                    'source_text': doc.get('source_text', "SOURCE TEXT NOT AVAILABLE"),
                    'future_effective_date': doc.get('future_effective_date', "N/A"),
                    'highlights': doc.highlights('text')
                })
        return documents
