import React from 'react'

import FontAwesomeIcon from '@fortawesome/react-fontawesome'
import faPencilAlt from '@fortawesome/fontawesome-free-solid/faPencilAlt'

class ReadRaspberryConfiguration extends React.Component {

  constructor(props) {
    super(props);

    this.updateRaspberryConfiguration = this.updateRaspberryConfiguration.bind(this);
  }

  updateRaspberryConfiguration() {
    this.props.onUpdate('readerRaspberry')
  }

  render() {

    return (<div className="row">
      <div className="col-md-10">
        <label htmlFor="raspberryModel">Modello Raspberry</label>
        <p id="raspberryModel">
          <b>{this.props.raspberry.model}</b>
        </p>
      </div>
      <div className="col-md-2">
        <button type="submit" className="btn btn-success" onClick={this.updateRaspberryConfiguration}>
          <FontAwesomeIcon icon={faPencilAlt}/>
          &nbsp;Modifica
        </button>
      </div>
    </div>)
  }

}

export default ReadRaspberryConfiguration
