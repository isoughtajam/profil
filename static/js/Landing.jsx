import React from 'react';

import App from './App';
import FrontDoor from './FrontDoor';

export default class Landing extends React.Component {
  constructor(props) {
    super(props);
    this.enter = this.enter.bind(this);
    this.state = {status: 'frontdoor'};
  }

  enter() {
    this.setState({status: 'app'});
  }

  render() {
    if (this.state.status == 'frontdoor') {
      var experience = <FrontDoor enter={this.enter} />;
    } else {
      var experience = <App />;
    }

    return (
      <div id="at-isoughtajam">
        {experience}
      </div>
    );
  }
}