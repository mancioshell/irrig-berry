import React from 'react';

import promise from 'es6-promise'
promise.polyfill()
import fetch from 'isomorphic-fetch'

import Electrovalve from './electrovalve'

class CreateElectrovalve extends React.Component {

  constructor(props) {
    super(props);
    this.state = {electrovalve: props.electrovalve};
    this.create = this.create.bind(this);
  }

  create(newElectrovalve) {
    let { last_water, watering, timetable, sensor_pin, humidity_threshold, ...others } = newElectrovalve;

    let electrovalve;

    switch (newElectrovalve.mode) {
      case 'manual':
        electrovalve = Object.assign({}, others)
        break;
      case 'automatic':
        electrovalve = Object.assign({}, {sensor_pin:sensor_pin}, {humidity_threshold:humidity_threshold}, others)
        break;
      case 'scheduled':
        electrovalve = Object.assign({}, {timetable: timetable}, others)
        break;
      default:
        break;
    }

    fetch('/api/electrovalves', {
      credentials: 'same-origin',
      method: 'POST',
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify(electrovalve)
    }).then(response => {
      if (response.ok) {
        return response.json()
      } else {
        throw response.json()
      }
    }).then(response => {
      electrovalve._id = response.id;
      this.setState({electrovalve : electrovalve});
      this.props.onCreate(electrovalve)
    })
  }

  render() {
    return (
      <Electrovalve onSubmit={this.create} electrovalve={this.state.electrovalve}></Electrovalve>
    );
  }

}

export default CreateElectrovalve;
