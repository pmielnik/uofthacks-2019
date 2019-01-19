import React from "react";
import axios from "axios";
import Rating from "../assets/rating.png";
import "./Dashboard.css";

export default class Dashboard extends React.Component {
  constructor(props) {
    super(props);
    this.state = { odometer: 0 };

    this.getOdometer = this.getOdometer.bind(this);
  }
  componentDidMount() {
    this.getOdometer(this.props.info.id);
  }
  getOdometer(id) {
    return axios
      .get(`${process.env.REACT_APP_SERVER}/odometer?vehicleId=${id}`)
      .then(res => {
        console.log(res.data);
        this.setState({ odometer: res.data.data.distance });
      });
  }

  render() {
    console.log(this.state.odometer);
    return (
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
                Your car is{" "}
                <b>
                  {this.props.info.make} {this.props.info.model}{" "}
                  {this.props.info.year}
                </b>
              </p>
              <img
                className="car-avatar"
                src="https://insideevs.com/wp-content/uploads/2017/12/IMG_20171214_164551-e1529516907468.jpg"
                alt="Car"
              />

              <table className="car-metrics">
                <tbody>
                  <tr>
                    <td className="metric-title">
                      <b>Mileage</b>
                    </td>
                    <td className="metric">
                      {this.state.odometer.toFixed(0)} km
                    </td>
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
                </tbody>
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
  }
}
