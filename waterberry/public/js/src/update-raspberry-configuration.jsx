import React from 'react'

import promise from 'es6-promise'
promise.polyfill()
import fetch from 'isomorphic-fetch'

import FontAwesomeIcon from '@fortawesome/react-fontawesome'
import faCheckCircle from '@fortawesome/fontawesome-free-solid/faCheckCircle'

class UpdateRaspberryConfiguration extends React.Component {

  constructor(props) {
    super(props);

    this.updateRaspberryConfiguration = this.updateRaspberryConfiguration.bind(this);
  }

  componentDidMount() {}

  updateRaspberryConfiguration() {
    fetch('/api/raspberry', {
      credentials: 'same-origin',
      method: 'PUT',
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify(this.props.raspberry)
    }).then(response => {
      if (response.ok) {
        return response.json()
      } else {
        throw response.json()
      }
    }).then(response => {
      this.props.onSave('readerRaspberry')
    })
  }

  render() {

    return (<div className="row">
      <div className="col-md-12">

        <form className="form-inline">

          <label className="sr-only" htmlFor="raspberryPiId">Tipologia Raspberry</label>
          <select className="form-control mb-2 mr-sm-2" id="raspberry" onChange={this.props.onChange} value={this.props.raspberry.model}>
            {
              (() => {
                return this.props.raspberry.models.map((model, index) => {
                  return (<option key={model.id} value={model.id}>{model.name}</option>)
                });
              })()
            }
          </select>

          <button type="submit" className="btn btn-primary mb-2" onClick={this.updateRaspberryConfiguration}>
            <FontAwesomeIcon icon={faCheckCircle}/>
            &nbsp;Salva
          </button>

        </form>


      </div>
    </div>)
  }

}

export default UpdateRaspberryConfiguration
