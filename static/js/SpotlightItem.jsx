import React from 'react';

import SpotlightItemTitle from './SpotlightItemTitle';
import SpotlightItemImg from './SpotlightItemImg';
import SpotlightItemBlurb from './SpotlightItemBlurb';

export default class SpotlightItem extends React.Component {
  render() {
    return (
      <div className="spotlightItem" id={this.key}>
        <SpotlightItemTitle 
          name={this.props.name}
        />
        <SpotlightItemImg
          url={this.props.url}
          img={this.props.img}
        />
        <SpotlightItemBlurb
          text={this.props.text}
        />
      </div>
    );
  }
}
