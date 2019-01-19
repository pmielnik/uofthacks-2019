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
      <div className="left-col">
        <div className="car-info">
          <p className="car-header">
            You own a <b>{info.model}</b>
          </p>
          <img
            className="car-avatar"
            src="https://insideevs.com/wp-content/uploads/2017/12/IMG_20171214_164551-e1529516907468.jpg"
            alt="Car image"
          />

          <table className="car-metrics">
            <tr>
              <td className="metric-title">
                <b>Mileage</b>
              </td>
              <td className="metric">{info.odometer.data} km</td>
            </tr>
            <tr>
              <td className="metric-title">
                <b>Current location</b>
              </td>
              <td className="metric">24 Valley Dr., CA</td>
            </tr>
            <tr>
              <td className="metric-title">
                <b>Estimated Trade-in Value</b>
              </td>
              <td className="metric">$ 10,000</td>
            </tr>
          </table>
        </div>
      </div>
      {/* <button
        onClick={() => {
          console.log(odometer);
        }}
      >
        Odometr
      </button> */}
    </div>
  </div>
);
