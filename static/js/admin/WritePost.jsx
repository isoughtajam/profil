import React from 'react';

export default class WritePost extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      postTitle: "",
      postDate: "",
      postBody: ""
    };
    this.handleChange = this.handleChange.bind(this);
    // this.handleSubmit = this.handleSubmit.bind(this);
  }

  handleChange(event) {
    const target = event.target;
    const value = target.value;
    const name = target.name;

    this.setState({
      [name]: value
    });
  }

  render() {
    return(
      <div id="writePost">
        <form id="writePostForm" method="post">
          <div class="writePostInput">
            <label class="clear-right">Post Title:</label>
            <input
              id="postTitleInput"
              type="text"
              name="postTitle"
              value={this.state.postTitle}
              onChange={this.handleChange} 
            />
          </div>
          <div class="writePostInput">
            <label class="clear-right">Post Date:</label>
            <input
              id="postDateInput"
              type="text"
              name="postDate"
              value={this.state.postDate}
              onChange={this.handleChange}
            />
          </div>
          <div class="writePostInput">
            <label class="clear-right">Post Body:</label>
            <textarea
              id="postBodyInput"
              name="postBody"
              form="writePostForm"
              value={this.state.postBody}
              onChange={this.handleChange}
            />
          </div>
          <div class="writePostSubmit">
            <input type="submit" value="Submit" />
          </div>
        </form>
      </div>
    )
  }
}