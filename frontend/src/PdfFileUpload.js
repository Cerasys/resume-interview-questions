// PdfFileUpload.js

import React from "react";
import "./PdfFileUpload.css"; // Import the CSS file

const PdfFileUpload = ({
  file1,
  file2,
  handleFile1Change,
  handleFile2Change,
  handleSubmit,
}) => {
  // Determine whether to enable the submit button
  const isSubmitDisabled = !file1;

  return (
    <div className="pdf-upload-container">
      <h1>Upload PDF Files</h1>
      <div className="file-input">
        <label htmlFor="file1">Upload File 1 (PDF):</label>
        <input
          type="file"
          id="file1"
          accept=".pdf"
          onChange={handleFile1Change}
        />
      </div>
      {/* <div className="file-input">
        <label htmlFor="file2">Upload File 2 (PDF) (optional):</label>
        <input
          type="file"
          id="file2"
          accept=".pdf"
          onChange={handleFile2Change}
        />
      </div> */}
      <div className="selected-files">
        <h2>Selected Files:</h2>
        {file1 && <p>File 1: {file1.name}</p>}
        {file2 && <p>File 2: {file2.name}</p>}
      </div>
      <button onClick={handleSubmit} disabled={isSubmitDisabled}>
        Submit
      </button>{" "}
      {/* Disable the button */}
    </div>
  );
};

export default PdfFileUpload;
