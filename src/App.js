import React from 'react';
import './App.css';

import logoSVG from './img/logo.svg';
import steps from './img/steps.png';
import dragdrop from './img/dragdrop.png';

function App() {
  // Assume images are in the public/img folder
  const logoPath = require("./img/logo.png"); // Path relative to the JS file
  const stepsPath = '/img/steps.png';
  const dropIconPath = '/img/dragdrop.png'; // Using dragdrop.png for the inner icon as requested

  return (
    <div className="App">
      <header className="App-header">
        <img src={logoSVG} className="App-logo" alt="Soldered Image Converter Logo" />
        <div className="Board-selector">
          <label htmlFor="boardSelect">Select board:</label>
          <select id="boardSelect" name="board">
            <option value="inkplate6motion">Inkplate 6 MOTION</option>
            {/* Add other board options here if needed */}
          </select>
        </div>
      </header>

      <main className="App-main">
        <p className="Intro-text">
          Soldered Image Converter is a simple tool used to generate Arduino-compatible C++ code for displaying images on displays from Soldered Electronics.
        </p>

        <img src={steps} className="Steps-image" alt="Steps: 1. Upload, 2. Convert, 3. Upload" />

        <div className="Dropzone">
          <h2>Drag and drop your files here</h2>
          <p className="File-info">
            Supported file types: .jpg, .png, .bmp <br />
            10 files max.
          </p>
          <img src={dragdrop} className="Dropzone-icon" alt="Drag and drop placeholder" />
          <p className="Or-divider">OR</p>
          <button className="Browse-button">BROWSE</button>
        </div>
      </main>
    </div>
  );
}

export default App;