import React from 'react';

export default class NavItem extends React.Component {
  constructor(props) {
    super(props);
    this.handleNavigation = this.handleNavigation.bind(this);
  }

  handleNavigation() {
    this.props.navigate(this.props.name);
  }
  render() {
    if (this.props.content == this.props.name) {
      return (
        <div className="navItem">
          <a className="navLink" onClick={this.handleNavigation}><p className="navText">> {this.props.name}</p></a>
        </div>
      );
    } else {
      return (
        <div className="navItem">
          <a className="navLink" onClick={this.handleNavigation}><p className="navText">{this.props.name}</p></a>
        </div>
      );
    }
  }
}