import React from 'react';
import ReactDOM from 'react-dom';

import Container from './Container';
import Footer from './Footer';

export default class App extends React.Component {
  constructor(props) {
    super(props);
    this.navigate = this.navigate.bind(this);
    this.state = {content: 'mine'};
  }

  navigate(dest) {
    this.setState({content: dest});
  }

  render() {
    return (
      <div id="app">
        <div className="parallax_top">
          <div id="title">
            <span className="display-name">Gautam Joshi</span>
          </div>
        </div>
        <Container 
          content={content}
        />
      </div>
    );
  }
}