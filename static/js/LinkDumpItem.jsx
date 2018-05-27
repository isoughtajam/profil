import React from 'react';

import LinkDumpItemTitle from './LinkDumpItemTitle';

export default class LinkDumpItem extends React.Component {
  render() {
    return (
      <div className="link-dump-item" id={this.key}>
        <LinkDumpItemTitle 
          name={this.props.name}
          url={this.props.url}
        />
      </div>
    );
  }
}