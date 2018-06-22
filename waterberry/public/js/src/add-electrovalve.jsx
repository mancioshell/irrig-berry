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
    return (<div className="card fig-container card-dashed text-center">
      <div className="fig-overlay">
        <button className="btn btn-primary" onClick={this.new}>
          <i className="fas fa-plus"></i>
          &nbsp;Aggiungi
        </button>
      </div>
    </div>);
  }
}

export default AddElectrovalve;
