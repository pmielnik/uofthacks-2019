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
      currentAddress: "",
      last24HoursKM: Math.floor(Math.random() * 60 + 10),
      lastWeekKM: Math.floor(Math.random() * 380 + 115),
      emission: 0,
      lightbulbHours: 0,
      treesToPlant: 0,
      odometer: 0,
      imgSrc: null,
      resaleValue: 0,
      filter: "24 hours",
      location: { lat: 0, lon: 0 }
    };

    this.getEmission = this.getEmission.bind(this);
    this.getPrice = this.getPrice.bind(this);
    this.getLightBulb = this.getLightBulb.bind(this);
    this.getOdometer = this.getOdometer.bind(this);
    this.getLocation = this.getLocation.bind(this);
    this.getTrees = this.getTrees.bind(this);
    this.generateImageURL = this.generateImageURL.bind(this);
    this.setFilter = this.setFilter.bind(this);
  }

  componentDidMount() {
    let carName =
      this.props.info.make + " " + this.props.model + " " + this.props.year;
    this.getOdometer(this.props.info.id);
    this.getEmission(this.props.info.id);
    this.getTrees(this.props.info.id);
    this.getLightBulb(this.props.info.id);
    this.getLocation(this.props.info.id);
    this.getPrice(this.props.info.id);
    this.generateImageURL(carName);
  }

  getPrice(id) {
    return axios
      .get(`${process.env.REACT_APP_SERVER}/price?vehicleId=${id}`)
      .then(res => {
        this.setState({
          resaleValue: res.data.price.toFixed(0)
        });
      });
  }

  generateImageURL(name) {
    return axios
      .get(`${process.env.REACT_APP_SERVER}/get-image?carModel=${name}`)
      .then(res => {
        this.setState({
          imgSrc: res.data.imageURL
        });
      });
  }

  getEmission(id) {
    return axios
      .get(`${process.env.REACT_APP_SERVER}/co2emission?vehicleId=${id}`)
      .then(res => {
        this.setState({
          emission: res.data.CO2emission.toFixed(2)
        });
      });
  }

  getLightBulb(id) {
    return axios
      .get(`${process.env.REACT_APP_SERVER}/lightbulbs?vehicleId=${id}`)
      .then(res => {
        this.setState({
          lightbulbHours: res.data.LightBulbHours.toFixed(2)
        });
      });
  }

  getTrees(id) {
    return axios
      .get(`${process.env.REACT_APP_SERVER}/treestoplant?vehicleId=${id}`)
      .then(res => {
        this.setState({
          treesToPlant: res.data.TreesToPlant.toFixed(2)
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
        this.setState(
          {
            location: res.data.data
          },
          () => {
            this.getAddress();
          }
        );
      });
  }

  getAddress() {
    return axios
      .get(
        `https://maps.googleapis.com/maps/api/geocode/json?latlng=${
          this.state.location.latitude
        },${this.state.location.longitude}&key=${
          process.env.REACT_APP_GOOGLE_MAPS_API_KEY
        }
    `
      )
      .then(res => {
        this.setState({
          currentAddress: res.data.results[0].formatted_address
        });
      })
      .catch(err => {
        console.log("ERROR: " + err);
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
                    <td className="metric">{this.state.currentAddress}</td>
                  </tr>
                  <tr>
                    <td className="metric-title">
                      <b>Estimated Trade-in Value</b>
                    </td>
                    <td className="metric">
                      ${this.state.resaleValue && this.state.resaleValue}
                    </td>
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
                You've driven{" "}
                <b>
                  {this.state.filter === "24 hours" && this.state.last24HoursKM}
                  {this.state.filter === "week" && this.state.lastWeekKM}
                </b>{" "}
                kilometers in the past {this.state.filter}.
              </div>
              <div className="timeline">
                <p>
                  <b>Your places:</b>
                </p>
                {this.state.location.latitude > 0 && (
                  <Timeline
                    lat={this.state.location.latitude}
                    lng={this.state.location.longitude}
                    pastDay={this.state.last24HoursKM}
                    pastWeek={this.state.lastWeekKM}
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
                      <i>Community average 50.40</i>
                    </p>
                  </div>
                </div>
                <div className="eco-metrics">
                  <img className="small-icon" src={BulbIcon} alt="Bulb" />
                  <div className="small-col">
                    <p>Light bulb (hours)</p>
                    <p className="metrics-val">
                      <b>
                        {this.state.lightbulbHours && this.state.lightbulbHours}
                      </b>
                    </p>
                    <p>
                      <i>Community average 857.65</i>
                    </p>
                  </div>
                </div>
                <div className="eco-metrics">
                  <img className="small-icon" src={TreeIcon} alt="Tree" />
                  <div className="small-col">
                    <p>Trees to offset</p>
                    <p className="metrics-val">
                      <b>
                        {this.state.treesToPlant && this.state.treesToPlant}
                      </b>
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
