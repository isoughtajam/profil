import React from 'react';

import SearchResults from './SearchResults';

export default class SearchResultsContainer extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      results: []
    };
  }

  /*
  * Capture search term and call /get-search-results/<search term> endpoint to get results for display
  * 
  */
  componentDidMount() {
    var searchTerms = document.getElementById('term_string').content;
    fetch("/get-search-results/" + searchTerms)
        .then(res => res.json())
        .then(jsonRes => this.setState(jsonRes));
  }

  render() {
    var resultCount = this.state.results.length;
    var resultNoun = resultCount == 1 ? 'result' : 'results';
    return (
      <div id="search-results-container">
        <p class="search-header">Found {resultCount} {resultNoun}.</p>
        <SearchResults 
          results={this.state.results}
        />
      </div>
    )
  }
}