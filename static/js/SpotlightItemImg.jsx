import React from 'react';

export default class SpotlightItemImg extends React.Component {
  render() {
    return(
      <div className="spotlightItemImgDiv">
        <a href={this.props.url}>
          <img src={this.props.img} className="spotlightItemImg"></img>
        </a>
      </div>
    )
  }
}