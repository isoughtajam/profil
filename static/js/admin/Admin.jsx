import React from 'react';

import AdminNav from './AdminNav';
import AdminContainer from './AdminContainer';

export default class Admin extends React.Component {
  constructor(props) {
    super(props);
    this.navigate = this.navigate.bind(this);
    this.state = {
      adminPage: "write_post"
    };
  }

  navigate(adminPage) {
    this.setState({adminPage: adminPage});
  }

  render() {
    return(
      <div id="admin">
        <AdminNav navigate={this.navigate} />
        <AdminContainer adminPage={this.state.adminPage} />
      </div>
    )
  }
}