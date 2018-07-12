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
    var href = "/" + this.props.name;
    if (this.props.content == this.props.name) {
      return (
        <div className="nav-item">
          <a className="nav-link" href={href}>
            <p className="nav-text-animated">{this.props.name}</p></a>
        </div>
      );
    } else {
      return (
        <div className="nav-item">
          <a className="nav-link" href={href}>
            <p className="nav-text">{this.props.name}</p></a>
        </div>
      );
    }
  }
}