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
    var search_terms = document.getElementById('term_string').content;
    fetch("/get-search-results/" + search_terms)
        .then(res => res.json())
        .then(jsonRes => this.setState(jsonRes));
  }

  render() {
    var result_count = this.state.results.length;
    return (
      <div id="search-results-container">
        <p class="search-header">Found {result_count} result(s).</p>
        <SearchResults 
          results={this.state.results}
        />
      </div>
    )
  }
}