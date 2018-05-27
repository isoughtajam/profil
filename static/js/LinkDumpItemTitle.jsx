import React from 'react';

export default class LinkDumpItemTitle extends React.Component {
  render() {
    return(
      <div className="link-dump-item-title-div">
        <a  target='_blank' href={this.props.url} className="link-dump-item-title">{this.props.name}</a>
      </div>
    )
  }
}