import React from 'react';

export default class NavItem extends React.Component {
  render () {
    return (
      <div className="navItem">
        <a className="navLink" href=""><p className="navText">{this.props.name}</p></a>
      </div>
    );
  }
}