import React from 'react';

class AddElectrovalve extends React.Component {

  constructor(props) {
    super(props);
    this.new = this.new.bind(this);
  }

  new(e){
    this.props.onNew()
  }

  render() {
    return (<div className="card fig-container">
      <div className="card-header text-black bg-light">Nuova Elettrovalvola</div>
      <img className="card-img-top fig-card" src="img/electrovalve.jpg" alt="Card image cap"/>
      <div className="fig-overlay">
        <a href="#" className="btn btn-primary" onClick={this.new}>
          <i className="fas fa-plus"></i>
          &nbsp;Aggiungi
        </a>
      </div>
    </div>);
  }
}

export default AddElectrovalve;
