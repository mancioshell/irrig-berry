import React from 'react'

import promise from 'es6-promise'
promise.polyfill()
import fetch from 'isomorphic-fetch'

import FontAwesomeIcon from '@fortawesome/react-fontawesome'
import faCheckCircle from '@fortawesome/fontawesome-free-solid/faCheckCircle'

class UpdateSensorConfiguration extends React.Component {

  constructor(props) {
    super(props);

    this.updateSensorConfiguration = this.updateSensorConfiguration.bind(this);
  }

  componentDidMount() {}

  updateSensorConfiguration() {
    fetch('/api/sensors', {
      credentials: 'same-origin',
      method: 'PUT',
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify(this.props.sensor)
    }).then(response => {
      if (response.ok) {
        return response.json()
      } else {
        throw response.json()
      }
    }).then(response => {
      this.props.onSave('readerSensor')
    })
  }

  render() {
    return (<div className="row">
      <div className="col-md-12">
        <form className="form-inline">

          <label className="sr-only" htmlFor="humidity_temperatureId">Pin Sensore Temperatura / Umidit&agrave;</label>
          <select className="form-control mb-2 mr-sm-2" id="humidity_temperatureId" onChange={this.props.onChangePin} value={this.props.sensor.pin}>
            {
              (() => {
                return this.props.pins.map((pin, index) => {
                  return (<option key={index} value={pin}>{pin}</option>)
                });
              })()
            }
          </select>

          <label className="sr-only" htmlFor="sensor_typeId">Tipologia Sensore</label>
          <select className="form-control mb-2 mr-sm-2" id="sensor_typeId" onChange={this.props.onChangeType} value={this.props.sensor.type}>
            {
              (() => {
                return this.props.sensor.types.map((type, index) => {
                  return (<option key={index} value={type}>{type}</option>)
                });
              })()
            }
          </select>

          <button type="submit" className="btn btn-primary mb-2" onClick={this.updateSensorConfiguration}>
            <FontAwesomeIcon icon={faCheckCircle}/>
            &nbsp;Salva
          </button>
        </form>
      </div>
    </div>)
  }

}

export default UpdateSensorConfiguration
