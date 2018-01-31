import React from 'react';
import Ghadyaal from 'ghadyaal';

import Spotlight from './Spotlight';
import NavItem from './NavItem';

var spotlightData = require('../json/spotlight.json');
var spotlights = spotlightData['items'];

var projectionData = require('../json/projection.json');
var projections = projectionData['items'];

export default class Container extends React.Component {
  constructor(props) {
    super(props);
    this.navigate = this.navigate.bind(this);
    this.state = {content: 'mine'};
  }

  navigate(dest) {
    this.setState({content: dest});
  }

  render() {
    const content = this.state.content;
    console.log("this.state.content == " + content);
    if (this.state.content == "mine") {
      var contentType = projections;
    } else {
      var contentType = spotlights;
    }
    return (
      <div id="container">
        <div id="nav">
          <a href="https://www.npmjs.com/package/ghadyaal" target="_blank"><Ghadyaal
            backgroundColor="#444"
            strokeColor="#dcdcdc"
            numeralSize={40}
          /></a>
          <NavItem
            name="mine"
            content={content}
            navigate={this.navigate}
          />
          <NavItem
            name="others"
            content={content}
            navigate={this.navigate}
          />
        </div>
        <Spotlight
          spotlights={contentType}
        />
      </div>
    )
  }
}
