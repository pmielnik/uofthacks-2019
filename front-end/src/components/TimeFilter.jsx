import React from "react";
import "./TimeFilter.css";

function TimeFilter(props) {
  return (
    <React.Fragment>
      <input
        type="radio"
        value={props.value}
        className="def-time-filter"
        name="radio"
        onClick={props.onClick}
        id={props.id}
      />
      <label className="time-filter" for={props.id}>
        {props.title}
      </label>
    </React.Fragment>
  );
}

export default TimeFilter;
