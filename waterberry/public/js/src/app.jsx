import React from 'react';
import ReactDOM from 'react-dom';

import promise from 'es6-promise'
promise.polyfill()
import fetch from 'isomorphic-fetch'

import 'bootstrap/dist/css/bootstrap.css';
import 'bootstrap/dist/js/bootstrap.js';
import 'cssDir/app.css';

import Nav from './nav'
import Jumbotron from './jumbotron'
import ElectrovalveViewer from './electrovalve-viewer'

class App extends React.Component {

  constructor(props) {
    super(props);
    this.state = {
      electrovalves: []
    };

    this.addElectrovalve = this.addElectrovalve.bind(this);
    this.removeElectrovalve = this.removeElectrovalve.bind(this);
  }

  addElectrovalve(electrovalve) {
    this.setState({electrovalves: this.state.electrovalves.concat(electrovalve)})
  }

  removeElectrovalve(electrovalve) {
    let electrovalves = this.state.electrovalves.filter(elem => elem._id != electrovalve._id)
    this.setState({electrovalves: electrovalves})
  }

  componentDidMount() {

    fetch('/api/electrovalves', {
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
    }).then(response => {
      this.setState({electrovalves: response});
    })
  }

  render() {
    const newElectrovalve = {
      name: 'Nuova Elettrovalvola',
      duration: 1
    }
    const electrovalveList = this.state.electrovalves.map((electrovalve) => {
      return (<div key={electrovalve._id} className="col-md-3">
        <ElectrovalveViewer viewer="read" removeElectrovalve={this.removeElectrovalve} addElectrovalve={this.addElectrovalve} electrovalve={electrovalve}></ElectrovalveViewer>
      </div>)
    });

    return (<div id="parent">
      <div id="layout">
        <Nav></Nav>
        <Jumbotron></Jumbotron>
      </div>
      <div id="container" className="container-fluid">

        <div className="row">
          {electrovalveList}
          <div className="col-md-3">
            <ElectrovalveViewer viewer="new" addElectrovalve={this.addElectrovalve} electrovalve={newElectrovalve}></ElectrovalveViewer>
          </div>
        </div>

        <footer>
          <p>© Company 2017</p>
        </footer>
      </div>
    </div>);
  }
}

ReactDOM.render(<App/>, document.getElementById('root'));
