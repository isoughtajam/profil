import React from 'react';
import ReactDOM from 'react-dom';

const PostText = ({paragraphs}) => (
  <div id="post-body">
    {paragraphs.map(paragraph => (
      <p className='post-paragraph' dangerouslySetInnerHTML={ {__html: paragraph} } />
    ))}
  </div>
);

export default PostText;