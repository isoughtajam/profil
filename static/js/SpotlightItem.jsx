import React from 'react';

export default class SpotlightItem extends React.Component {
  render() {
    return (
      <div className="spotlightItem" id={this.key}>
        <p className="spotlightItemTitle">{this.props.name}</p>
        <a href={this.props.url}>
          <img src={this.props.img} className="spotlightItemImg"></img>
        </a>
      </div>
    );
  }
}
