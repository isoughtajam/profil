import React from 'react';

export default class Spotlight extends React.Component {
  render () {
    return (
      <div className="spotlight" id={this.key}>
        <p className="spotlightTitle">{this.props.name}</p>
        <a href={this.props.url}>
          <img src={this.props.img} className="spotlightImg"></img>
        </a>
      </div>
    );
  }
}
