import React from 'react';
import ReactDOM from 'react-dom';

import PostParagraph from './PostParagraph';

const PostText = ({paragraphs}) => (
  <div id="post-body">
    {paragraphs.map(paragraph => (
      <PostParagraph
        key={paragraph.paraId}
        paraText={paragraph.paraText}
      />
    ))}
  </div>
);

export default PostText;