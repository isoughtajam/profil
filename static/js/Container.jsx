import React from 'react';

import Spotlight from './Spotlight';


var spotlightData = require('../json/spotlight.json');
var spotlights = spotlightData['items'];

var projectionData = require('../json/projection.json');
var projections = projectionData['items'];

export default class Container extends React.Component {
  constructor(props) {
    super(props);
  }

  render() {
    if (this.props.content == 'mine') {
      return (
        <Spotlight
          spotlights={projections}
        />
      );
    } else {
      return (
        <Spotlight
          spotlights={spotlights} 
        />
      )
    }
  }
}
