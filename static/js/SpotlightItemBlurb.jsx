import React from 'react';

export default class SpotlightItemBlurb extends React.Component {
  render() {
    return(
      <div className="spotlightItemBlurbDiv">
        <p className="spotlightItemBlurb">{this.props.text}</p>
      </div>
    )
  }
}