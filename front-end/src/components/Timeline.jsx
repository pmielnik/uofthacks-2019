import React, { Component } from "react";
import { Map, InfoWindow, Marker, GoogleApiWrapper } from "google-maps-react";

const style = {
  width: "33%",
  height: "50%"
};
export class Timeline extends React.Component {
  render() {
    console.log(this.props);
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
      />
    );
  }
}

export default GoogleApiWrapper({
  apiKey: process.env.REACT_APP_GOOGLE_MAPS_API_KEY
})(Timeline);
