import React from 'react';

export default class FrontDoor extends React.Component {
  constructor(props) {
    super(props);
  }

  render() {
    return (
      <div id="frontdoor">
        <a className="centered" onClick={this.props.enter}>welcome</a>
      </div>
    );
  }
}