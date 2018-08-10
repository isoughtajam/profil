import React from 'react';

export default class SearchResultRecord extends React.Component {
  constructor(props) {
    super(props);
  }

  render() {
    var resultText = this.props.resultText;
    var postPath = '/blog/' + this.props.slug + '/';
    return (
      <div className="search-result-record" id={this.key}>
        <p dangerouslySetInnerHTML={ {__html: resultText} } />
        <p className="search-result-title">From <a href={postPath}>{this.props.postTitle}</a></p>
        <br />
      </div>
    );
  }
}