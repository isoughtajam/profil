import React from 'react';

export default class SearchBar extends React.Component {
  constructor(props) {
    super(props);
  }

  render() {
    return (
      <div id="search-bar">
        <form id="searchForm" method="get" action="/search/">
          <input
            id="terms"
            type="text"
            name="terms"
            placehlder="search..."
          />
        </form>
      </div>
    )
  }
}