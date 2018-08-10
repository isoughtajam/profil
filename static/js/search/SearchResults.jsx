import React from 'react';

import SearchResultRecord from './SearchResultRecord';

const SearchResults = ({results}) => (
  <div id="search-results">
    {results.map(result => (
      <SearchResultRecord 
        key={result.id}
        slug={result.slug}
        resultText={result.search_result}
        postTitle={result.post_title}
      />
    ))}
  </div>
)

export default SearchResults;