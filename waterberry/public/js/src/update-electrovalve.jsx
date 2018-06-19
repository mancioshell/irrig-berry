import React from 'react';

import promise from 'es6-promise'
promise.polyfill()
import fetch from 'isomorphic-fetch'

import Electrovalve from './electrovalve'

class UpdateElectrovalve extends React.Component {

  constructor(props) {
    super(props);
    this.state = {
      electrovalve: props.electrovalve
    };
    this.update = this.update.bind(this);
  }

  update(updated_electrovalve) {
    let { last_water, watering, timetable, pin_di, pin_do, pin_clk, pin_cs, humidity_threshold, ...others } = updated_electrovalve;
    let electrovalve;

    switch (updated_electrovalve.mode) {
      case 'manual':
        electrovalve = Object.assign({}, others)
        break;
      case 'automatic':
        electrovalve = Object.assign({}, {pin_di:pin_di}, {pin_do:pin_do}, {pin_clk:pin_clk}, {pin_cs:pin_cs}, {humidity_threshold:humidity_threshold}, others)
        break;
      case 'scheduled':
        electrovalve = Object.assign({}, {timetable: timetable}, others)
        break;
      default:
        break;
    }

    fetch('/api/electrovalves/' + this.state.electrovalve._id, {
      credentials: 'same-origin',
      method: 'PUT',
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
      this.setState({electrovalve: electrovalve});
      this.props.onUpdate(electrovalve)
    })
  }

  render() {
    return (<Electrovalve onSubmit={this.update} electrovalve={this.state.electrovalve}></Electrovalve>);
  }
}

export default UpdateElectrovalve;
