import React from 'react';
import ReactDOM from 'react-dom';

import Spotlight from './Spotlight';

/*
Spot should be a carousel
*/


const Spot = ({spotlights}) => (
  <div id="spot">
    {spotlights.map(spotlight => (
      <Spotlight 
        key={spotlight.id}
        name={spotlight.name}
        img={spotlight.img}
        url={spotlight.url}
      />
    ))}
  </div>
);

export default Spot;