// QuestionList.js

import React from "react";
import "./QuestionList.css"; // Import the CSS file

const QuestionList = ({ questions }) => {
  return (
    <div className="question-list-container">
      <h2>Received Questions:</h2>
      <ul className="question-list">
        {questions.map((question, index) => (
          <li key={index}>{question}</li>
        ))}
      </ul>
    </div>
  );
};

export default QuestionList;
