import React from 'react';

import promise from 'es6-promise'
promise.polyfill()
import fetch from 'isomorphic-fetch'

import ElectrovalveViewer from './electrovalve-viewer'

class ElectrovalveList extends React.Component {

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
      return (<div key={electrovalve._id} className="col-sm-4">
        <ElectrovalveViewer viewer="read" removeElectrovalve={this.removeElectrovalve} addElectrovalve={this.addElectrovalve} electrovalve={electrovalve}></ElectrovalveViewer>
      </div>)
    });

    return (
      <div className="row">
        {electrovalveList}
        <div className="col-sm-4">
          <ElectrovalveViewer viewer="new" addElectrovalve={this.addElectrovalve} electrovalve={newElectrovalve}></ElectrovalveViewer>
        </div>
      </div>
    );
  }

}

export default ElectrovalveList;
