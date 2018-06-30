import React from 'react';
import ReactDOM from 'react-dom';

import LinkDumpItem from './LinkDumpItem';

const LinkDump = ({links}) => (
  <div className="link-dump">
    {links.map(link => (
      <LinkDumpItem 
        key={link.id}
        name={link.name}
        url={link.url}
        text={link.text}
        blurb={link.blurb}
      />
    ))}
  </div>
);

export default LinkDump;