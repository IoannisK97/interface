// Plot.js
import React from 'react';
import Plot from 'react-plotly.js';

const PlotComponent = ({ data }) => {
  return <Plot data={data} />;
};

export default PlotComponent;