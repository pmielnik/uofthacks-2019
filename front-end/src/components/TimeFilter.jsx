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
        defaultChecked={props.checked}
      />
      <label className="time-filter" htmlFor={props.id}>
        {props.title}
      </label>
    </React.Fragment>
  );
}

export default TimeFilter;
