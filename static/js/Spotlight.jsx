import React from 'react';
import ReactDOM from 'react-dom';

import SpotlightItem from './SpotlightItem';


const Spotlight = ({spotlights}) => (
  <div id="spotlight">
    {spotlights.map(spotlightItem => (
      <SpotlightItem 
        key={spotlightItem.id}
        name={spotlightItem.name}
        img={spotlightItem.img}
        url={spotlightItem.url}
        text={spotlightItem.text}
      />
    ))}
  </div>
);

export default Spotlight;