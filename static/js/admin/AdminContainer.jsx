import React from 'react';

import WritePost from './WritePost';

export default class AdminContainer extends React.Component {
  constructor(props) {
    super(props);
  }

  render() {
    return(
      <div id="adminPage">
        <WritePost />
      </div>
    )
  }
}