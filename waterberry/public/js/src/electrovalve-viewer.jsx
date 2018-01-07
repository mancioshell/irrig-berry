import React from 'react';

import CreateElectrovalve from './create-electrovalve'
import UpdateElectrovalve from './update-electrovalve'
import AddElectrovalve from './add-electrovalve'
import ReadElectrovalve from './read-electrovalve'

class ElectrovalveViewer extends React.Component {

  constructor(props) {
    super(props);
    this.state = {
      electrovalve: props.electrovalve
    };
    this.state.viewer = props.viewer;
    this.onNew = this.onNew.bind(this);
    this.onCreate = this.onCreate.bind(this);
    this.onUpdate = this.onUpdate.bind(this);
    this.onRead = this.onRead.bind(this);
    this.onDelete = this.onDelete.bind(this);
  }

  onNew() {
    this.setState({viewer: 'create'});
  }

  onCreate(electrovalve) {
    //add in list
    this.props.addElectrovalve(electrovalve)
    //reset state
    this.setState({
      electrovalve: {
        name: 'Nuova Elettrovalvola',
        duration: 1
      }
    });
    this.setState({viewer: 'new'});
  }

  onUpdate(electrovalve) {
    this.setState({electrovalve: electrovalve, viewer: 'read'});
  }

  onRead() {
    this.setState({viewer: 'update'});
  }

  onDelete(electrovalve) {
    this.props.removeElectrovalve(electrovalve)
  }

  render() {

    return ((() => {
      switch (this.state.viewer) {
        case 'new':
          return <AddElectrovalve onNew={this.onNew} electrovalve={this.state.electrovalve}></AddElectrovalve>
        case 'create':
          return <CreateElectrovalve onCreate={this.onCreate} electrovalve={this.state.electrovalve}></CreateElectrovalve>
        case 'update':
          return <UpdateElectrovalve onUpdate={this.onUpdate} electrovalve={this.state.electrovalve}></UpdateElectrovalve>
        case 'read':
          return <ReadElectrovalve onDelete={this.onDelete} onRead={this.onRead} electrovalve={this.state.electrovalve}></ReadElectrovalve>;
        default:
          return <AddElectrovalve onNew={this.onNew} electrovalve={this.state.electrovalve}></AddElectrovalve>
      }
    })());
  }
}

export default ElectrovalveViewer;
