import React from 'react';
import ReactDOM from 'react-dom';

import Container from './Container';
import NavItem from './NavItem';
import Ghadyaal from 'ghadyaal';

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
    const content = this.state.content;
    console.log("this.state.content == " + content);
    return (
      <div id="app">
        <div id="nav">
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
        <Ghadyaal />
        <Container 
          content={content}
        />
      </div>
    );
  }
}