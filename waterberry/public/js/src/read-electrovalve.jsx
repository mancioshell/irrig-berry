import React from 'react';

import promise from 'es6-promise'
promise.polyfill()
import fetch from 'isomorphic-fetch'
import * as moment from 'moment';
moment.locale("it");

import FontAwesomeIcon from '@fortawesome/react-fontawesome'
import faTrashAlt from '@fortawesome/fontawesome-free-solid/faTrashAlt'
import faMinus from '@fortawesome/fontawesome-free-solid/faMinus'
import faSpinner from '@fortawesome/fontawesome-free-solid/faSpinner'
import faTint from '@fortawesome/fontawesome-free-solid/faTint'
import faPencilAlt from '@fortawesome/fontawesome-free-solid/faPencilAlt'
import faClock from '@fortawesome/fontawesome-free-solid/faClock'
import faMagic from '@fortawesome/fontawesome-free-solid/faMagic'

import {subscribeToElectrovalveData, unSubscribeToElectrovalveData} from './socket';

class ReadElectrovalve extends React.Component {

  constructor(props) {
    super(props);
    this.state = {
      electrovalve: props.electrovalve
    };

    this.water = this.water.bind(this);
    this.delete = this.delete.bind(this);
  }

  onRead() {
    this.props.onRead();
  }

  water() {
    fetch('/api/electrovalves/' + this.state.electrovalve._id, {
      credentials: 'same-origin',
      method: 'PATCH',
      headers: {
        "Content-Type": "application/json"
      }
    }).then(response => {
      if (response.ok) {
        return response.json()
      } else {
        throw response.json()
      }
    }).then(response => {
      this.state.electrovalve.watering = true;
      this.setState({electrovalve: this.state.electrovalve});
    })
  }

  componentDidMount() {  
    subscribeToElectrovalveData((err, data) => {
      for (let value of data) {
        if (value._id == this.state.electrovalve._id) {
          this.state.electrovalve.watering = value.watering;
          this.state.electrovalve.air_humidity = value.air_humidity;
          this.state.electrovalve.air_temperature = value.air_temperature;
          this.state.electrovalve.current_humidity = value.soil_humidity;
          this.state.electrovalve.last_water = value.last_water;

          this.setState({electrovalve: this.state.electrovalve});
        }
      }
    });
  }

  componentWillUnmount(){
    unSubscribeToElectrovalveData();
  }

  componentDidCatch(error, info) {}

  delete() {
    fetch('/api/electrovalves/' + this.state.electrovalve._id, {
      credentials: 'same-origin',
      method: 'DELETE',
      headers: {
        "Content-Type": "application/json"
      }
    }).then(response => {
      if (response.ok) {
        return response.json()
      } else {
        throw response.json()
      }
    }).then(response => {
      this.props.onDelete(this.state.electrovalve)
    })
  }

  render() {

    let current_humidity = this.state.electrovalve.current_humidity <= 13
      ? "14%"
      : this.state.electrovalve.current_humidity + "%";
    let humidity_threshold = this.state.electrovalve.humidity_threshold <= 13
      ? "14%"
      : this.state.electrovalve.humidity_threshold + "%";

    let current_humidity_percentage = this.state.electrovalve.current_humidity + "%";
    let humidity_threshold_percentage = this.state.electrovalve.humidity_threshold + "%";

    return (<div className="card card-container">
      <div className="card-header text-black bg-light">
        {this.state.electrovalve.name}
        <button type="button" className="btn btn-danger btn-sm float-right" onClick={this.delete}>
          <FontAwesomeIcon icon={faTrashAlt}/>
          &nbsp;Elimina
        </button>
      </div>
      <img className="card-img-top img-card" src="img/gerani.jpg" alt="Card image cap"/>
      <div className="card-body">
        <form>
          <div className="form-row">
            <div className="col-md-6 mb-3">
              <label htmlFor="electroValveId">Pin Elettrovalvola</label>
              <p>
                <b>{this.state.electrovalve.electrovalve_pin}</b>
              </p>
            </div>

            <div className="col-md-6 mb-3">
              <label htmlFor="durationId">Tempo di irrigazione</label>
              <p>
                <b>{this.state.electrovalve.duration}&nbsp;secondi</b>
              </p>
            </div>
          </div>

          {
            (() => {
              if (this.state.electrovalve.mode == 'automatic') {
                return (<div className="form-row">
                  <div className="col-md-6 mb-3">
                    <label htmlFor="pin_diId">Pin DI</label>
                    <p>
                      <b>{this.state.electrovalve.pin_di}</b>
                    </p>
                  </div>
                  <div className="col-md-6 mb-3">
                    <label htmlFor="pin_doId">Pin DO</label>
                    <p>
                      <b>{this.state.electrovalve.pin_do}</b>
                    </p>
                  </div>
                </div>)
              }
            })()
          }

          {
            (() => {
              if (this.state.electrovalve.mode == 'automatic') {
                return (<div className="form-row">
                  <div className="col-md-6 mb-3">
                    <label htmlFor="pin_clkId">Pin Clock</label>
                    <p>
                      <b>{this.state.electrovalve.pin_clk}</b>
                    </p>
                  </div>
                  <div className="col-md-6 mb-3">
                    <label htmlFor="pin_csId">Pin CS</label>
                    <p>
                      <b>{this.state.electrovalve.pin_cs}</b>
                    </p>
                  </div>
                </div>)
              }
            })()
          }

          {
            (() => {
              if (this.state.electrovalve.mode == 'scheduled') {
                const timetables = this.state.electrovalve.timetable.map((timetable, index) => {
                  return (<tr key={index}>
                    <td>{index}</td>
                    <td>{timetable.time}</td>
                    <td>{timetable.day}</td>
                  </tr>)
                })
                return (<div className="form-row">
                  <p>Irrigazioni Schedulate:
                  </p>
                  <div className="col-md-12 mb-3">

                    <table className="table table-striped table-sm">
                      <thead>
                        <tr>
                          <th scope="col">#</th>
                          <th scope="col">Orario</th>
                          <th scope="col">Giorno</th>
                        </tr>
                      </thead>
                      <tbody>
                        {timetables}
                      </tbody>
                    </table>
                  </div>
                </div>)
              }
            })()
          }

          <div className="form-row">
            <div className="col-md-6 mb-3">
              <label htmlFor="humidityId">Umidità Aria </label>
                <p>
                  {
                    this.state.electrovalve.air_humidity
                      ? <b>{this.state.electrovalve.air_humidity}°</b>
                      : <span>
                          <FontAwesomeIcon icon={faMinus}/>
                        </span>
                  }
                </p>
            </div>

            <div className="col-md-6 mb-3">
              <label htmlFor="lastWaterId">Temperatura Aria </label>
              <p>
                {
                  this.state.electrovalve.air_temperature
                    ? <b>{this.state.electrovalve.air_temperature}°</b>
                    : <span>
                        <FontAwesomeIcon icon={faMinus}/>
                      </span>
                }
              </p>
            </div>
          </div>


          {
            (() => {
              if (this.state.electrovalve.mode == 'automatic') {
                return (<div className="form-row">
                  <div className="col-md-6 mb-3">
                    <label htmlFor="soilHumidityId">Umidità Terra</label>
                      {
                        this.state.electrovalve.current_humidity
                          ? <div className="progress">
                              <div className="progress-bar" id="soilHumidityId" role="progressbar" style={{
                                  width: current_humidity
                                }} aria-valuemin="0" aria-valuemax="100">{current_humidity_percentage}</div>
                            </div>
                          : <p>
                              <span>
                                <FontAwesomeIcon icon={faMinus}/>
                              </span>
                            </p>
                      }
                  </div>
                  <div className="col-md-6 mb-3">
                    <label htmlFor="tresholdId">Soglia Umidità</label>
                    <div className="progress">
                      <div className="progress-bar" id="tresholdId" role="progressbar" style={{
                          width: humidity_threshold
                        }} aria-valuemin="0" aria-valuemax="100">{humidity_threshold_percentage}</div>
                    </div>
                  </div>
                </div>)
              }
            })()
          }

          <div className="form-row">
            <div className="col-md-6 mb-3">
              <p>Modalità:
              </p>
              {
                (() => {
                  switch (this.state.electrovalve.mode) {
                    case 'automatic':
                      return <h6>
                        <span className="badge badge-primary">
                          <FontAwesomeIcon icon={faMagic}/>
                          &nbsp;Automatico
                        </span>
                      </h6>
                      break;
                    case 'scheduled':
                      return <h6>
                        <span className="badge badge-success">
                          <FontAwesomeIcon icon={faClock}/>
                          &nbsp;Temporizzato</span>
                      </h6>
                      break;
                    case 'manual':
                      return <h6>
                        <span className="badge badge-info">
                          <FontAwesomeIcon icon={faTint}/>
                          &nbsp;Manuale</span>
                      </h6>
                      break;
                    default:
                      return <h6>
                        <span className="badge badge-info">
                          <FontAwesomeIcon icon={faTint}/>
                          &nbsp;Manuale</span>
                      </h6>
                  }
                })()
              }

            </div>
            <div className="col-md-6 mb-3">
              <label htmlFor="lastWaterId">Ultima irrigazione:</label>
              <p>
                {
                  this.state.electrovalve.last_water
                    ? <b>{moment.utc(this.state.electrovalve.last_water).fromNow()}</b>
                    : <FontAwesomeIcon icon={faMinus}/>
                }

              </p>
            </div>
          </div>

          <div className="row">
            <div className="col-md-12">
              <button type="button" disabled={this.state.electrovalve.watering} className="btn btn-success" onClick={(e) => this.onRead()}>
                <FontAwesomeIcon icon={faPencilAlt}/>
                &nbsp;Modifica
              </button>

              &nbsp;

              <button type="button" disabled={this.state.electrovalve.watering} className="btn btn-primary" onClick={this.water}>

                {
                  this.state.electrovalve.watering
                    ? <FontAwesomeIcon icon={faSpinner} pulse/>
                    : <FontAwesomeIcon icon={faTint}/>
                }

                &nbsp;Innaffia
              </button>

            </div>
          </div>

        </form>

      </div>
    </div>);
  }

}

export default ReadElectrovalve;
