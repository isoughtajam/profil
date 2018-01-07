import React from 'react';
import ReactDOM from 'react-dom';

import Spot from './Spot';
import NavItem from './NavItem';

var spotlightData = require('../json/spotlight.json');
console.log(spotlightData);
var spotlights = spotlightData['items'];
console.log(spotlights);

export default class App extends React.Component {
  render () {
    return (
      <div id="app">
        <div id="nav">
          <NavItem name="mine" active={false} />
          <NavItem name="others" active={true} />
        </div>
        <Spot spotlights={spotlights} />
      </div>
    );
  }
}