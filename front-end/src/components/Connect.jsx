import React from "react";
import "./Connect.css";

export default ({ onClick }) => (
  <div className="app-page">
    <div className="middle-container">
      <h1 className="app-title">
        <span className="title-green-part">Green</span>icle
      </h1>
      <p className="app-desc">
        Greenicle helps you view car activity and reflect on your environmental
        impact while providing options to contribute to the community. Making
        the world a better place, one tree at a time.
      </p>
      <button className="app-button transparent" onClick={onClick}>
        CONNECT TO YOUR CAR
      </button>
    </div>
  </div>
);
