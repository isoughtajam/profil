import React from 'react';

import PostText from './PostText';
import PostNavLink from './PostNavLink';

export default class Post extends React.Component {
  constructor(props) {
    super(props);
  }

  render() {
    var prevLink = null;
    var nextLink = null;
    if (this.props.prevSlug != null) {
      prevLink = <PostNavLink 
                  navigatePost={this.props.navigatePost}
                  postSlug= {this.props.prevSlug}
                  text="prev" />;
    }
    if (this.props.nextSlug != null) {
      nextLink = <PostNavLink 
                  navigatePost={this.props.navigatePost}
                  postSlug= {this.props.nextSlug}
                  text="next" />;
    }
    return (
      <div className="post">
          <p className="post-title">{this.props.title}</p>
          <p className="post-date">{this.props.postDate}</p>
          <PostText 
            paragraphs={this.props.paragraphs}
          />
          <div className="post-nav">
            {prevLink}
            {nextLink}
          </div>
      </div>
    );
  }
}