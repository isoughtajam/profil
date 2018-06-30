import React from 'react';

export default class PostParagraph extends React.Component {
  constructor(props) {
    super(props);
  }

  render() {
    var paraText = this.props.paraText;
    return (
      <div className="post-paragraph" id={this.key}>
        <p className='post-paragraph'
          dangerouslySetInnerHTML={ {__html: paraText} } 
        />
      </div>
    );
  }
}