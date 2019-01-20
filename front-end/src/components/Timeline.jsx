import React, { Component } from "react";
import { Map, InfoWindow, Marker, GoogleApiWrapper } from "google-maps-react";

const style = {
  width: "33%",
  height: "50%"
};
export class Timeline extends React.Component {
  constructor(props) {
    super(props);
    this.state = { markers: [] };
  }

  componentDidMount() {
    let n = Math.floor((Math.random() * this.props.pastDay) / 10 + 2);
    let markers = [];

    for (let i = 0; i < n; i++) {
      var r = 500 / 111300, // = 100 meters
        y0 = this.props.lat,
        x0 = this.props.lng,
        u = Math.random(),
        v = Math.random(),
        w = r * Math.sqrt(u),
        t = 2 * Math.PI * v,
        x = w * Math.cos(t),
        y1 = w * Math.sin(t),
        x1 = x / Math.cos(y0);
      markers.push({ lat: y0 + y1, lng: x0 + x1 });
    }

    this.setState({ markers });
  }

  render() {
    console.log(this.state.markers);
    return (
      <Map
        google={this.props.google}
        style={style}
        zoom={14}
        initialCenter={{
          lat: this.props.lat,
          lng: this.props.lng
        }}
        fullscreenControl={false}
        scaleControl={false}
        streetViewControl={false}
        mapTypeControl={false}
        zoomControl={false}
      >
        {this.state.markers.map(marker => {
          let new_lat = marker.lat;
          let new_lng = marker.lng;
          return <Marker position={{ lat: new_lat, lng: new_lng }} />;
        })}
      </Map>
    );
  }
}

export default GoogleApiWrapper({
  apiKey: process.env.REACT_APP_GOOGLE_MAPS_API_KEY
})(Timeline);
