import React from 'react';

import LinkDump from './LinkDump';
import Post from './Post';

var otherLinksData = require('../../json/otherlinks.json');
var otherLinks = otherLinksData['items'];

var myLinksData = require('../../json/mylinks.json');
var myLinks = myLinksData['items'];

var socialLinksData = require('../../json/sociallinks.json');
var socialLinks = socialLinksData['items'];

export default class Container extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      title: "",
      slug: "",
      author: "",
      postDate: "",
      paragraphs: [],
      prevSlug: "",
      nextSlug: ""
    };
    this.navigatePost = this.navigatePost.bind(this);
    this.componentDidMount = this.componentDidMount.bind(this);
  }

  /*
  * Similar to id-based post getting, on mount the component will get the 
  *   data of the latest blog post and its next/prev slugs.
  * 
  * Nav links will use the next/prev slugs.
  * Post will be instantiated with the appropriate slug. Post will fetch the post
  *   data to display.
  */
  componentDidMount() {
    fetch("/latest-post")
      .then(res => res.json())
      .then(jsonRes => this.setState(jsonRes));

  }

  /*
  * Update state with current post id, previous and nextids
  */
  navigatePost(slug) {
    console.log("navigatePost");
    console.log(slug);
    fetch("/post/" + slug)
      .then(res => res.json())
      .then(jsonRes => this.setState(jsonRes));
  }

  render() {
    if (this.props.content == "blog") {
      return (
        <div id="container">
          <Post
            title={this.state.title}
            author={this.state.author}
            postDate={this.state.postDate}
            paragraphs={this.state.paragraphs}
            prevSlug={this.state.prevSlug}
            nextSlug={this.state.nextSlug}
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