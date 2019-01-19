import React from "react";
import Rating from "../assets/rating.png";
import "./Dashboard.css";

export default ({ info, odometer }) => (
  <div className="app-page">
    <div className="app-navbar">
      <h1 className="app-logo">
        <span className="title-green-part">Green</span>icle
      </h1>
      <div className="nav-user">
        <p>Hi, user@tesla.ca</p>
        <a className="nav-logout" href="/">
          <b>Logout</b>
        </a>
        <div className="user-rating">
          Community rating:{" "}
          <img className="rating-img" src={Rating} alt="Community rating" />
        </div>
      </div>
    </div>
    <div className="dashboard">
      <button
        onClick={() => {
          console.log(odometer);
        }}
      >
        Odometr
      </button>
    </div>
  </div>
);
