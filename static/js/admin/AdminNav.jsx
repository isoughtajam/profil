import React from 'react';

import NavItem from '../app/NavItem';

export default class AdminNav extends React.Component {
  constructor(props) {
    super(props);
  }

  render() {
    return(
      <div id="adminNav">
        <NavItem
          navigate={this.props.navigate}
          name="writePost" 
          content="none" 
        />
      </div>
    )
  }
}