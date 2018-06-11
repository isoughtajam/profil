import React from 'react';

import FrontDoor from './FrontDoor';

export default class Landing extends React.Component {
  constructor(props) {
    super(props);
  }

  render() {
    return (
      <div id="at-isoughtajam">
        <FrontDoor />
      </div>
    );
  }
}