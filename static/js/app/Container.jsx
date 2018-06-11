import React from 'react';

import LinkDump from './LinkDump';
import Post from './Post';

var otherLinksData = require('../../json/otherlinks.json');
var otherLinks = otherLinksData['items'];

var myLinksData = require('../../json/mylinks.json');
var myLinks = myLinksData['items'];

var socialLinksData = require('../../json/sociallinks.json');
var socialLinks = socialLinksData['items'];

var postData = require('../../json/posts.json');
var posts = postData['items'];

export default class Container extends React.Component {
  constructor(props) {
    super(props);
    var postIDs = this.getMaxPostIds(posts);
    this.navigatePost = this.navigatePost.bind(this);
    this.state = {
      post: postIDs.post,
      prevId: postIDs.prevId,
      nextId: null
    };
  }

  getMaxPostIds(items) {
    if (items.length <= 1) {
      return {
        post: posts[0],
        prevId: null,
        nextId: null
      };
    } else {
      posts = items.sort((a,b) => b.id - a.id);
      return {
        post: posts[0],
        prevId: posts[1].id,
        nextId: null
      };
    }
  }

  getPostPrevAndNextIDs(postId) {
    var post = posts.find(function(o){if(o.id == postId) {return o}});
    var index = posts.indexOf(post);
    var prevId = null;
    var nextId = null;
    if (index > 0) {
      nextId = posts[index - 1].id;
    }
    if (posts.length - 1 > index) {
      prevId = posts[index + 1].id;
    }
    return {
      post: post,
      prevId: prevId,
      nextId: nextId
    };
  }

  navigatePost(postId) {
    var IDs = this.getPostPrevAndNextIDs(postId);
    console.log(postId);
    this.setState(IDs);
  }

  render() {
    if (this.props.content == "blog") {
      return (
        <div id="container">
          <Post
            post={this.state.post}
            prevId={this.state.prevId}
            nextId={this.state.nextId}
            navigatePost={this.navigatePost}
          />
        </div>
      )
    } else {
      return (
        <div id="container">
          <div className="my-links">
            <p className="links-title">mine</p>
            <LinkDump
              links={myLinks}
            />
          </div>
          <div className="other-links">
            <p className="links-title">others</p>
            <LinkDump
              links={otherLinks}
            />
          </div>
          <div className="social-links">
            <p className="links-title">find me</p>
            <LinkDump
              links={socialLinks}
            />
          </div>
        </div>
      )
    }
  }
}