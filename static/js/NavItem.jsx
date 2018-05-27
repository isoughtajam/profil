import React from 'react';

export default class NavItem extends React.Component {
  constructor(props) {
    super(props);
    this.handleNavigation = this.handleNavigation.bind(this);
  }

  handleNavigation() {
    //console.log("this.props.name -> " + this.props.name)
    this.props.navigate(this.props.name);
  }
  render() {
    if (this.props.content == this.props.name) {
      return (
        <div className="nav-item">
          <button className="nav-link" onClick={this.handleNavigation}>
            <p className="nav-text-animated">{this.props.name}</p></button>
        </div>
      );
    } else {
      return (
        <div className="nav-item">
          <button className="nav-link" onClick={this.handleNavigation}>
            <p className="nav-text">{this.props.name}</p></button>
        </div>
      );
    }
  }
}