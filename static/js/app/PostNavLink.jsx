import React from 'react';

export default class PostNavLink extends React.Component {
  constructor(props) {
    super(props);
    this.prevNextNavigation = this.prevNextNavigation.bind(this);
  }

  prevNextNavigation() {
    this.props.navigatePost(this.props.postSlug);
  }

  render() {
    var dest = "/blog/" + this.props.postSlug;
    return (
      <div className="post-nav-link">
        <a className="pre-next-link"
          href={dest}
          >{this.props.text}</a>
      </div>
    );
  }
}
