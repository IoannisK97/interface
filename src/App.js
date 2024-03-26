import React, { useState, useEffect } from 'react';
import Plotly from 'plotly.js-basic-dist';
import createPlotlyComponent from 'react-plotly.js/factory';
import './App.css';
const Plot = createPlotlyComponent(Plotly);


const App = () => {
  const [functionString, setFunctionString] = useState('');
  const [epsilon, setEpsilon] = useState('');
  const [learningRate, setLearningRate] = useState('');
  const [rangeInput, setRangeInput] = useState('');
  const [learningRateType, setLearningRateType] = useState('regular');  
  const [maxIterations, setMaxIterations] = useState('10000');
  const [result, setResult] = useState(null);
  const [plotData, setPlotData] = useState(null);
  const [currentPoint, setCurrentPoint] = useState(null);
  const [iteration, setIteration] = useState(0);

  const plotLayout = {
    width: 800,
    height: 400,
  };
  

  const optimizeFunction = async () => {
    try {
      const response = await fetch('http://localhost:5000/api/gradient-descent', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          functionString,
          epsilon: parseFloat(epsilon),
          learningRate: parseFloat(learningRate),
          rangeInput: rangeInput.split(',').map(Number), 
          learningRateType: learningRateType,  
          maxIter: parseInt(maxIterations),
        }),
      });

      if (!response.ok) {
        throw new Error('Failed to optimize function');
      }

      const data = await response.json();

      const { xValues, yValues, pointsGradient } = data;

      setResult(data.result);

      const functionPlot = {
        x: xValues,
        y: yValues,
        type: 'scatter',
        mode: 'lines',
        name: 'Function',
      };

      const allPoints = pointsGradient.map(point => {
        return {
          x: [point[0]],
          y: [point[1]],
          type: 'scatter',
          mode: 'markers',
          name: 'Points',
        };
      });
      

      setPlotData([functionPlot,  { x: [], y: [], type: 'scatter', mode: 'markers', name: 'Points' }]);
      
      for (const point of allPoints) {
        setIteration(prevIteration => prevIteration + 1);
        setPlotData([functionPlot, point]);
        console.log("in the loop");

  
        setCurrentPoint(point);
        
        await new Promise((resolve) => setTimeout(resolve, 100));
      }

    } catch (error) {
      console.error('Error optimizing function:', error);
      setResult(null);
    }
  };

  useEffect(() => {
    optimizeFunction();
  }, []);


  return (
    <div>
      <h1 className='header'>Gradient Descent Interface</h1>

      <label className='label'>
        Function 'x':
        <input className='input-field'
          type="text"
          value={functionString}
          onChange={(e) => setFunctionString(e.target.value)}
        />
      </label>

      <label className='label'>
        epsilon:
        <input className='input-field'
          type="text"
          value={epsilon}
          onChange={(e) => setEpsilon(e.target.value)}
        />
      </label>

      <label className='label'> 
        learning rate:
        <input className='input-field'
          type="text"
          value={learningRate}
          onChange={(e) => setLearningRate(e.target.value)}
        />
      </label>

      <label className='label'>
        Learning Rate Type:
        <select className='select' value={learningRateType} onChange={(e) => setLearningRateType(e.target.value)}>
          <option value="regular">Regular</option>
          <option value="armijo">Armijo</option>
          <option value="adaptive">Adaptive</option>
          
        </select>
      </label>

      <label className='label'>
        range (comma-separated values, e.g., 0,10):
        <input className='input-field'
          type="text"
          value={rangeInput}
          onChange={(e) => setRangeInput(e.target.value)}
        />
      </label>
      
      

      <label className='label'> 
        Max Iterations:
        <input className='input-field'
          type="text"
          value={maxIterations}
          onChange={(e) => setMaxIterations(e.target.value)}
        />
      </label>

      <div className='header'>
        <button className="button" onClick={optimizeFunction}>Optimize Function</button>
      </div>

      <div id='plot' className="plot-container">
        {plotData && <Plot data={plotData} layout={plotLayout} key={plotData.length} />}
      </div>

      <div>
      {currentPoint  &&(
        <div className='header'> 
          <p >Iteration: {iteration}</p> 
          <p>Current Point: ({currentPoint.x[0]}, {currentPoint.y[0]})</p>
          
        </div>
      )}
      </div>
    </div>
  );
};

export default App;
