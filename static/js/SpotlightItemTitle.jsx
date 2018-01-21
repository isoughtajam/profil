import React from 'react';

export default class SpotlightItemTitle extends React.Component {
  render() {
    return(
      <div className="spotlightItemTitleDiv">
        <p className="spotlightItemTitle">{this.props.name}</p>
      </div>
    )
  }
}