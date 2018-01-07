import React from 'react';

class Timetable extends React.Component {

  constructor(props) {
    super(props);
    this.state = {
      time: props.time,
      day: props.day
    };
    this.handleChange = this.handleChange.bind(this);    
  }

  handleChange(event) {
    const target = event.target;
    const name = target.name;

    this.state[name] = target.value;
    this.setState(this.state);
    this.props.onUpdate(this.state, this.props.index)
  }

  render() {
    return (<div className="form-row">
      <div className="col-md-6 mb-3">
        <label htmlFor="time">Orario</label>
        <input name="time" onChange={this.handleChange} type="time" defaultValue={this.state.time} className="form-control form-control-sm" id="timeId" aria-describedby="time"/>
      </div>
      <div className="col-md-6 mb-3">
        <label htmlFor="exampleFormControlSelect1">Giorno:
        </label>
        <select name="day" onChange={this.handleChange} value={this.state.day} className="custom-select custom-select-sm">
          <option value="">Scegli il giorno</option>
          <option value="mon">Lunedì</option>
          <option value="tue">Martedì</option>
          <option value="wed">Mercoledì</option>
          <option value="thu">Giovedì</option>
          <option value="fri">Venerdì</option>
          <option value="sat">Sabato</option>
          <option value="sun">Domenica</option>
        </select>
      </div>

    </div>);
  }
}

export default Timetable;
