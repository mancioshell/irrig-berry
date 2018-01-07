import React from 'react';

import promise from 'es6-promise'
promise.polyfill()
import fetch from 'isomorphic-fetch'

import Timetable from './timetable'

class Electrovalve extends React.Component {

  constructor(props) {
    super(props);
    this.state = {
      electrovalve: props.electrovalve,
      electrovalvePins: [],
      sensorPins: []
    };

    this.onAdd = this.onAdd.bind(this);
    this.onUpdate = this.onUpdate.bind(this);
    this.onSubmit = this.onSubmit.bind(this);
    this.handleChange = this.handleChange.bind(this);
    this.handleElectrovalvePinSelect = this.handleElectrovalvePinSelect.bind(this);
    this.handleSensorPinSelect = this.handleSensorPinSelect.bind(this);
  }

  componentDidMount() {

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

      let electrovalvePins = [].concat(pins)
      let sensorPins = [].concat(pins)

      if (electrovalvePins.filter(pin => pin == this.state.electrovalve.electrovalve_pin).length <= 0)
        electrovalvePins = electrovalvePins.concat(this.state.electrovalve.electrovalve_pin)

      if (sensorPins.filter(pin => pin == this.state.electrovalve.sensor_pin).length <= 0)
        sensorPins = sensorPins.concat(this.state.electrovalve.sensor_pin)

      this.setState({electrovalvePins: electrovalvePins, sensorPins: sensorPins});
    })
  }

  handleChange(event) {
    const target = event.target;
    const name = target.name;
    const value = target.type === 'number'
      ? parseInt(target.value)
      : target.value

    this.state.electrovalve[name] = value;

    if (name == 'mode' && value == 'automatic')
      this.state.electrovalve.humidity_threshold = 1
    if (name == 'mode' && value == 'scheduled' && !this.state.electrovalve.timetable)
      this.state.electrovalve.timetable = [
        {
          time: '00:00',
          day: 'mon'
        }
      ]

    this.setState({electrovalve: this.state.electrovalve});
  }

  handleElectrovalvePinSelect(event) {
    let value = event.target.value

    let newSensorPins = this.state.sensorPins.filter(pin => {
      return pin != value
    }).filter(pin => {
      return pin != this.state.electrovalve.electrovalve_pin
    }).concat(this.state.electrovalve.electrovalve_pin)

    let electrovalve = Object.assign({}, this.state.electrovalve);
    electrovalve.electrovalve_pin = value

    this.setState({sensorPins: newSensorPins, electrovalve: electrovalve});
  }

  handleSensorPinSelect(event) {
    let value = event.target.value

    let newElectrovalvePins = this.state.electrovalvePins.filter(pin => {
      return pin != value
    }).filter(pin => {
      return pin != this.state.electrovalve.sensor_pin
    }).concat(this.state.electrovalve.sensor_pin)

    let electrovalve = Object.assign({}, this.state.electrovalve);
    electrovalve.sensor_pin = value

    this.setState({electrovalvePins: newElectrovalvePins, electrovalve: electrovalve});
  }

  onAdd() {
    this.state.electrovalve.timetable = this.state.electrovalve.timetable.concat({time: '00:00', day: 'mon'})
    this.setState({electrovalve: this.state.electrovalve});
  }

  onUpdate(timetable, index) {
    this.state.electrovalve.timetable = this.state.electrovalve.timetable.map((elem, i) => {
      return i == index
        ? timetable
        : elem;
    })
    this.setState({electrovalve: this.state.electrovalve});
  }

  onSubmit() {
    this.props.onSubmit(this.state.electrovalve)
  }

  render() {

    return (<div className="card card-container">
      <div className="card-header text-black bg-light">
        {this.state.electrovalve.name}
      </div>
      <img className="card-img-top img-card" src="img/gerani2.jpg" alt="Card image cap"/>
      <div className="card-body">
        <form>

          <div className="form-row">
            <div className="col-md-6 mb-3">
              <label htmlFor="nameId">Nome Elettrovalvola</label>
              <input name="name" onChange={this.handleChange} type="text" defaultValue={this.state.electrovalve.name} className="form-control form-control-sm" id="nameId" aria-describedby="name"/>
            </div>
          </div>

          <div className="form-row">
            <div className="col-md-6 mb-3">
              <label htmlFor="electroValveId">Pin Elettrovalvola
              </label>
              <select name="electrovalve_pin" id="electrovalve_pin" onChange={this.handleElectrovalvePinSelect} value={this.state.electrovalve.electrovalve_pin} className="custom-select custom-select-sm">
                <option value="">Scegli il pin</option>
                {
                  (() => {
                    return this.state.electrovalvePins.map((pin, index) => {
                      return (<option key={index} value={pin}>{pin}</option>)
                    });
                  })()
                }
              </select>
            </div>

            <div className="col-md-6 mb-3">
              <label htmlFor="durationId">Tempo di irrigazione</label>
              <input name="duration" min="1" max="60" onChange={this.handleChange} type="number" defaultValue={this.state.electrovalve.duration} className="form-control form-control-sm" id="durationId" aria-describedby="duration"/>
            </div>
          </div>

          {
            (() => {
              if (this.state.electrovalve.mode == 'automatic') {
                return (<div className="form-row">
                  <div className="col-md-6 mb-3">
                    <label htmlFor="sensorId">Pin sensore
                    </label>
                    <select name="sensor_pin" id="sensor_pin" onChange={this.handleSensorPinSelect} value={this.state.electrovalve.sensor_pin} className="custom-select custom-select-sm">
                      <option value="">Scegli il pin</option>
                        {
                          (() => {
                            return this.state.sensorPins.map((pin, index) => {
                              return (<option key={index} value={pin}>{pin}</option>)
                            });
                          })()
                        }
                    </select>
                  </div>
                  <div className="col-md-6 mb-3">
                    <label htmlFor="tresholdId">Soglia Umidità</label>
                    <input name="humidity_threshold" min="1" max="100" onChange={this.handleChange} type="number" defaultValue={this.state.electrovalve.humidity_threshold} className="form-control form-control-sm" id="tresholdId" aria-describedby="treshold"/>
                  </div>
                </div>)
              }
            })()
          }

          {
            (() => {
              if (this.state.electrovalve.mode == 'scheduled') {
                const timetables = this.state.electrovalve.timetable.map((timetable, index) => {
                  return (<Timetable onUpdate={this.onUpdate} index={index} time={timetable.time} day={timetable.day} key={index}></Timetable>)
                })
                return timetables;
              }
            })()
          }

          {
            this.state.electrovalve.mode == 'scheduled'
              ? <div className="form-group">
                  <label htmlFor="mode">Modalità irrigazione:
                  </label>
                  <div className="input-group">
                    <select name="mode" id="mode" onChange={this.handleChange} value={this.state.electrovalve.mode} className="custom-select custom-select-sm">
                      <option value="">Scegli la modalità</option>
                      <option value="manual">Manuale</option>
                      <option value="automatic">Automatico</option>
                      <option value="scheduled">Temporizzato</option>
                    </select>
                    <div className="input-group-append">
                      <button className="btn btn-primary btn-sm" type="button" onClick={this.onAdd}>
                        <i className="fas fa-plus"></i>
                        &nbsp;Aggiungi
                      </button>
                    </div>
                  </div>
                </div>

              : <div className="form-group">
                  <label htmlFor="mode">Modalità irrigazione:
                  </label>
                  <select name="mode" id="mode" onChange={this.handleChange} value={this.state.electrovalve.mode} className="custom-select custom-select-sm">
                    <option value="">Scegli la modalità</option>
                    <option value="manual">Manuale</option>
                    <option value="automatic">Automatico</option>
                    <option value="scheduled">Temporizzato</option>
                  </select>
                </div>
          }

          <button type="button" className="btn btn-primary" onClick={this.onSubmit}>
            <i className="fas fa-check-circle"></i>
            &nbsp;Salva
          </button>

        </form>

      </div>
    </div>);
  }

}

export default Electrovalve;
