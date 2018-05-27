import React from 'react';

export default class PostNavLink extends React.Component {
  constructor(props) {
    super(props);
    this.prevNextNavigation = this.prevNextNavigation.bind(this);
  }

  prevNextNavigation() {
    this.props.navigatePost(this.props.postId);
  }

  render() {
    return (
      <div className="post-nav-link">
        <button className="pre-next-link" 
           onClick={this.prevNextNavigation}
          >{this.props.text}</button>
      </div>
    );
  }
}