import React from 'react';
import ReactDOM from 'react-dom';
import Ghadyaal from 'ghadyaal';

import Container from './Container';
import Footer from './Footer';
import NavItem from './NavItem';
import SearchBar from './SearchBar';

export default class App extends React.Component {
  constructor(props) {
    super(props);
    this.navigate = this.navigate.bind(this);
    var content = document.getElementById('content-type').content;
    this.state = {content: content};
  }

  navigate(dest) {
    this.setState({content: dest});
  }

  render() {
    return (
      <div id="app">
        <div id="nav">
          <a href="https://www.npmjs.com/package/ghadyaal" target="_blank"><Ghadyaal
            backgroundColor="#555"
            strokeColor="#ccc"
            numeralSize={30}
          /></a>
          <SearchBar />
          <NavItem
            name="blog"
            content={this.state.content}
          />
          <NavItem
            name="links"
            content={this.state.content}
          />
          <div className="webring-nav">
            <a href='http://webring.xxiivv.com/#random' target='_blank'><img className="webring" src='../../images/icon.white.svg'/></a>
          </div>
        </div>
        <Container 
          content={this.state.content}
        />
        <Footer />
      </div>
    );
  }
}