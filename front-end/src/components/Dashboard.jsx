import React from "react";
import axios from "axios";
import TimeFilter from "./TimeFilter";

import Timeline from "./Timeline";
import CarIcon from "../assets/car.svg";
import BulbIcon from "../assets/bulb.svg";
import TreeIcon from "../assets/tree.svg";
import Rating from "../assets/rating.png";
import "./Dashboard.css";

export default class Dashboard extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      emission: 0,
      odometer: 0,
      imgSrc: null,
      filter: "24 hours",
      location: { lat: 0, lon: 0 }
    };

    this.getEmission = this.getEmission.bind(this);
    this.getOdometer = this.getOdometer.bind(this);
    this.getLocation = this.getLocation.bind(this);
    this.generateImageURL = this.generateImageURL.bind(this);
    this.setFilter = this.setFilter.bind(this);
  }

  componentDidMount() {
    let carName =
      this.props.info.make + " " + this.props.model + " " + this.props.year;
    this.getOdometer(this.props.info.id);
    this.getEmission(this.props.info.id);
    this.getLocation(this.props.info.id);
    this.generateImageURL(carName);
  }

  generateImageURL(name) {
    return axios
      .get(`${process.env.REACT_APP_SERVER}/get-image?carModel=${name}`)
      .then(res => {
        console.log(res.data.imageURL);
        this.setState({
          imgSrc: res.data.imageURL
        });
      });
  }

  getEmission(id) {
    return axios
      .get(`${process.env.REACT_APP_SERVER}/co2emission?vehicleId=${id}`)
      .then(res => {
        console.log(res.data);
        this.setState({
          emission: res.data.CO2emission.toFixed(2)
        });
      });
  }

  getOdometer(id) {
    return axios
      .get(`${process.env.REACT_APP_SERVER}/odometer?vehicleId=${id}`)
      .then(res => {
        this.setState({
          odometer: res.data.data.distance.toFixed(0)
        });
      });
  }

  getLocation(id) {
    return axios
      .get(`${process.env.REACT_APP_SERVER}/location?vehicleId=${id}`)
      .then(res => {
        this.setState({
          location: res.data.data
        });
      });
  }

  setFilter(filter) {
    this.setState({
      filter
    });
  }

  render() {
    return (
      <div className="app-page">
        <div className="app-navbar">
          <h1 className="app-logo">
            <span className="title-green-part">Green</span>icle
          </h1>
          <div className="nav-user">
            <p>Hi, user@{this.props.info.make.toLowerCase()}.ca</p>
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
              {this.state.imgSrc && (
                <img className="car-avatar" src={this.state.imgSrc} alt="Car" />
              )}

              <table className="car-metrics">
                <tbody>
                  <tr>
                    <td className="metric-title">
                      <b>Mileage</b>
                    </td>
                    <td className="metric">{this.state.odometer} km</td>
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
          <div className="summary">
            <p className="dashboard-title">
              <b>Summary Statistics</b>
            </p>
            <div className="time-stats">
              <div className="time-filter-container">
                <p>
                  <b>Time filter</b>
                </p>
                <TimeFilter
                  title="Last 24 Hours"
                  id="daily-filter"
                  onClick={() => {
                    this.setFilter("24 hours");
                  }}
                  checked
                />
                <TimeFilter
                  title="Last week"
                  id="weekly-filter"
                  onClick={() => {
                    this.setFilter("week");
                  }}
                />
              </div>
              <div className="filtered-mileage">
                You've driven <b>{this.state.odometer}</b> kilometers in the
                past {this.state.filter}.
              </div>
              <div className="timeline">
                <p>
                  <b>Your places:</b>
                </p>
                {this.state.location.latitude > 0 && (
                  <Timeline
                    lat={this.state.location.latitude}
                    lng={this.state.location.longitude}
                  />
                )}
              </div>
            </div>
            <div className="eco-impact">
              <p className="green eco-title">
                <b>Your footprint</b>
              </p>
              <div className="metrics-container">
                <div className="eco-metrics">
                  <img className="small-icon" src={CarIcon} alt="Car" />
                  <div className="small-col">
                    <p>Total CO2 emission (tonnes)</p>
                    <p className="metrics-val">
                      <b>{this.state.emission && this.state.emission}</b>
                    </p>
                    <p>
                      <i>Community average 2.70</i>
                    </p>
                  </div>
                </div>
                <div className="eco-metrics">
                  <img className="small-icon" src={BulbIcon} alt="Bulb" />
                  <div className="small-col">
                    <p>Light bulb (hours)</p>
                    <p className="metrics-val">
                      <b>181.8</b>
                    </p>
                    <p>
                      <i>Community average 133</i>
                    </p>
                  </div>
                </div>
                <div className="eco-metrics">
                  <img className="small-icon" src={TreeIcon} alt="Tree" />
                  <div className="small-col">
                    <p>Trees to offset</p>
                    <p className="metrics-val">
                      <b>0.6</b>
                    </p>
                    <p>
                      <a
                        className="nav-logout underlined"
                        href="https://treecanada.ca/"
                      >
                        <i>Plant a tree now!</i>
                      </a>
                    </p>
                  </div>{" "}
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    );
  }
}
