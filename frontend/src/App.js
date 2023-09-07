import React, { useState } from "react";
import PdfFileUpload from "./PdfFileUpload";
import QuestionList from "./QuestionList";
import "./App.css";

function App() {
  const [file1, setFile1] = useState(null);
  const [file2, setFile2] = useState(null);
  const [questions, setQuestions] = useState([]);

  const handleSubmit = () => {
    if (!file1) {
      alert("Please select both PDF files before submitting.");
      return;
    }

    const formData = new FormData();
    formData.append("file1", file1);
    // formData.append("file2", file2);

    fetch("/api/upload", {
      method: "POST",
      body: formData,
    })
      .then((response) => response.json())
      .then((data) => {
        alert("Files uploaded successfully!");
        // You can handle the server response here
      })
      .catch((error) => {
        console.error("Error uploading file:", error);
        alert("Error uploading files. Please try again.");
      });

    // Simulate receiving questions from the backend (replace with actual API call)
    const receivedQuestions = [
      "Question 1: What is your experience with React?",
      "Question 2: Explain the difference between var, let, and const in JavaScript.",
      // Add more questions as needed
    ];

    setQuestions(receivedQuestions);
  };

  const handleFile1Change = (e) => {
    const selectedFile = e.target.files[0];
    if (selectedFile && selectedFile.type === "application/pdf") {
      setFile1(selectedFile);
    } else {
      alert("Please select a valid PDF file for File 1.");
    }
  };

  const handleFile2Change = (e) => {
    const selectedFile = e.target.files[0];
    if (selectedFile) {
      if (selectedFile.type === "application/pdf") {
        setFile2(selectedFile);
      } else {
        alert("Please select a valid PDF file for File 2.");
      }
    } else {
      // If no file is selected for the second input, set file2 to null
      setFile2(null);
    }
  };

  return (
    <div className="App">
      <h1>Persona AI Interview Question Builder</h1>
      <PdfFileUpload
        file1={file1}
        file2={file2}
        handleFile1Change={handleFile1Change}
        handleFile2Change={handleFile2Change}
        handleSubmit={handleSubmit} // Pass the handleSubmit function
      />
      {file1 && <p>File 1: {file1.name}</p>}
      {file2 && <p>File 2: {file2.name}</p>}

      {/* Render the QuestionList component */}
      {questions.length > 0 && <QuestionList questions={questions} />}
    </div>
  );
}

export default App;
