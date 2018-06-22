import React from 'react'

import FontAwesomeIcon from '@fortawesome/react-fontawesome'
import faPencilAlt from '@fortawesome/fontawesome-free-solid/faPencilAlt'

class ReadSensorConfiguration extends React.Component {

  constructor(props) {
    super(props);

    this.updateSensorConfiguration = this.updateSensorConfiguration.bind(this);
  }

  updateSensorConfiguration() {
    this.props.onUpdate('readerSensor')
  }

  render() {

    return (<div className="row">
      <div className="col-md-6">
        <label htmlFor="sensorType">Modello Sensore</label>
        <p id="sensorType">
          <b>{this.props.sensor.type}</b>
        </p>
      </div>
      <div className="col-md-4">
        <label htmlFor="sensorPin">Pin Sensore</label>
        <p id="sensorPin">
          <b>{this.props.sensor.pin}</b>
        </p>
      </div>
      <div className="col-md-2">
        <button type="submit" className="btn btn-success" onClick={this.updateSensorConfiguration}>
          <FontAwesomeIcon icon={faPencilAlt}/>
          &nbsp;Modifica
        </button>
      </div>
    </div>)
  }

}

export default ReadSensorConfiguration
