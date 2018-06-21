import React from 'react';

import promise from 'es6-promise'
promise.polyfill()
import fetch from 'isomorphic-fetch'

import ReadSensorConfiguration from './read-sensor-configuration'
import ReadRaspberryConfiguration from './read-raspberry-configuration'
import UpdateSensorConfiguration from './update-sensor-configuration'
import UpdateRaspberryConfiguration from './update-raspberry-configuration'

class Configuration extends React.Component {

  constructor(props) {
    super(props);
    this.state = {
      raspberry: {
        models: [],
        model: ""
      },
      sensor: {
        types: [],
        type: "",
        pin: ""
      },
      pins: [],
      reader: {
        readerRaspberry: true,
        readerSensor: true
      }
    };

    this.saveConfiguration = this.saveConfiguration.bind(this);
    this.updateConfiguration = this.updateConfiguration.bind(this);

    this.onChangeRaspberryConfiguration = this.onChangeRaspberryConfiguration.bind(this)
    this.onChangeSensorTypeConfiguration = this.onChangeSensorTypeConfiguration.bind(this)
    this.onChangeSensorPinConfiguration = this.onChangeSensorPinConfiguration.bind(this)

  }

  componentDidMount() {

    fetch('/api/raspberry', {
      credentials: 'same-origin',
      method: 'GET',
      headers: {
        "Content-Type": "application/json"
      }
    }).then(response => {
      if (response.ok) {
        return response.json()
      } else {
        throw response.json()
      }
    }).then(raspberry => {
      this.setState({raspberry: raspberry});
    })

    fetch('/api/pins', {
      credentials: 'same-origin',
      method: 'GET',
      headers: {
        "Content-Type": "application/json"
      }
    }).then(response => {
      if (response.ok) {
        return response.json()
      } else {
        throw response.json()
      }
    }).then(pins => {
      this.setState({pins: pins});

      fetch('/api/sensors', {
        credentials: 'same-origin',
        method: 'GET',
        headers: {
          "Content-Type": "application/json"
        }
      }).then(response => {
        if (response.ok) {
          return response.json()
        } else {
          throw response.json()
        }
      }).then(sensor => {
        this.setState({sensor: sensor});
        let pins = this.state.pins.concat(sensor.pin);
        this.setState({pins: pins});
      })
      
    });
  }

  onChangeRaspberryConfiguration(event) {
    let value = event.target.value;
    let raspberry = Object.assign({}, this.state.raspberry);
    raspberry.model = value
    this.setState({raspberry: raspberry});
  }

  onChangeSensorTypeConfiguration(event) {
    let value = event.target.value;
    let sensor = Object.assign({}, this.state.sensor);
    sensor.type = value
    this.setState({sensor: sensor});
  }

  onChangeSensorPinConfiguration(event) {
    let value = event.target.value;
    let sensor = Object.assign({}, this.state.sensor);
    sensor.pin = value
    this.setState({sensor: sensor});
  }

  saveConfiguration(type) {
    let state = this.state.reader[type] = true
    this.setState({reader: this.state.reader});
  }

  updateConfiguration(type) {
    this.state.reader[type] = false
    this.setState({reader: this.state.reader});
  }

  render() {

    return (<div className="row">
      <div className="col-md-6 offset-md-3">
        {
          !this.state.reader.readerRaspberry
            ? <UpdateRaspberryConfiguration
            onSave={this.saveConfiguration}
            onChange={this.onChangeRaspberryConfiguration}
            raspberry={this.state.raspberry}>
          </UpdateRaspberryConfiguration>
            : <ReadRaspberryConfiguration
            onUpdate={this.updateConfiguration}
            raspberry={this.state.raspberry}>
          </ReadRaspberryConfiguration>
        }

        {
          !this.state.reader.readerSensor
            ? <UpdateSensorConfiguration
            onSave={this.saveConfiguration}
            onChangeType={this.onChangeSensorTypeConfiguration}
            onChangePin={this.onChangeSensorPinConfiguration}
            sensor={this.state.sensor}
            pins={this.state.pins}>
          </UpdateSensorConfiguration>
            : <ReadSensorConfiguration
            onUpdate={this.updateConfiguration}
            sensor={this.state.sensor}>
          </ReadSensorConfiguration>
        }

      </div>
    </div>);
  }

}

export default Configuration;
