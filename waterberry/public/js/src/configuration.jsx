import React from 'react';

import promise from 'es6-promise'
promise.polyfill()
import fetch from 'isomorphic-fetch'

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
      pins: []
    };

    this.handleRaspberryModel = this.handleRaspberryModel.bind(this);
    this.handleSensorModel = this.handleSensorModel.bind(this);
    this.handlePins = this.handlePins.bind(this);
    this.updateRaspberryConfiguration = this.updateRaspberryConfiguration.bind(this);
    this.updateSensorConfiguration = this.updateSensorConfiguration.bind(this);
  }

  handleRaspberryModel(event) {
    let value = event.target.value;
    let raspberry = Object.assign({}, this.state.raspberry);
    raspberry.model = value
    this.setState({raspberry: raspberry});
  }

  handleSensorModel(event) {
    let value = event.target.value;
    let sensor = Object.assign({}, this.state.sensor);
    sensor.type = value
    this.setState({sensor: sensor});
  }

  handlePins(event) {
    let value = event.target.value;
    let sensor = Object.assign({}, this.state.sensor);
    sensor.pin = value
    this.setState({sensor: sensor});
  }

  updateRaspberryConfiguration() {
    fetch('/api/raspberry', {
      credentials: 'same-origin',
      method: 'PUT',
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify(this.state.raspberry)
    }).then(response => {
      if (response.ok) {
        return response.json()
      } else {
        throw response.json()
      }
    }).then(response => {})
  }

  updateSensorConfiguration() {
    fetch('/api/sensors', {
      credentials: 'same-origin',
      method: 'PUT',
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify(this.state.sensor)
    }).then(response => {
      if (response.ok) {
        return response.json()
      } else {
        throw response.json()
      }
    }).then(response => {})
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
      console.log(raspberry);
      this.setState({raspberry: raspberry});
    })

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
      console.log(sensor);
      this.setState({sensor: sensor});
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
      console.log(pins);
      this.setState({pins: pins});
    });
  }

  render() {

    return (<div className="row">
      <div className="col-md-6 offset-md-3">

        <form className="form-inline">

          <div className="form-group">
            <label htmlFor="humidity_temperatureId">Pin Sensore Temperatura / Umidit&agrave;</label>
            <select className="form-control" id="humidity_temperatureId" onChange={this.handlePins} value={this.state.sensor.pin}>
              {
                (() => {
                  return this.state.pins.map((pin, index) => {
                    return (<option key={index} value={pin}>{pin}</option>)
                  });
                })()
              }
            </select>
          </div>

          <div className="form-group">
            <label htmlFor="sensor_typeId">Tipologia Sensore</label>
            <select className="form-control" id="sensor_typeId" onChange={this.handleSensorModel} value={this.state.sensor.type}>
              {
                (() => {
                  return this.state.sensor.types.map((type, index) => {
                    return (<option key={index} value={type}>{type}</option>)
                  });
                })()
              }
            </select>
          </div>

          <button type="submit" className="btn btn-primary" onClick={this.updateSensorConfiguration}>Salva</button>
        </form>

        <form className="form-inline">
          <div className="form-group">
            <label htmlFor="raspberryPiId">Tipologia Raspberry</label>
            <select className="form-control" id="raspberryPiId" onChange={this.handleRaspberryModel} value={this.state.raspberry.model}>
              {
                (() => {
                  return this.state.raspberry.models.map((model, index) => {
                    return (<option key={model.id} value={model.id}>{model.name}</option>)
                  });
                })()
              }
            </select>
          </div>

          <button type="submit" className="btn btn-primary" onClick={this.updateRaspberryConfiguration}>Salva</button>
        </form>

      </div>
    </div>);

  }

}

export default Configuration;
