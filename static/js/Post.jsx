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
    if (this.props.prevId != null) {
      prevLink = <PostNavLink 
                  navigatePost={this.props.navigatePost}
                  postId= {this.props.prevId}
                  text="prev" />;
    }
    if (this.props.nextId != null) {
      nextLink = <PostNavLink 
                  navigatePost={this.props.navigatePost}
                  postId= {this.props.nextId}
                  text="next" />;
    }
    return (
      <div className="post">
          <p className="post-title">{this.props.post.title}</p>
          <p className="post-date">{this.props.post.date}</p>
          <PostText 
            paragraphs={this.props.post.paragraphs}
          />
          <div className="post-nav">
            {prevLink}
            {nextLink}
          </div>
      </div>
    );
  }
}