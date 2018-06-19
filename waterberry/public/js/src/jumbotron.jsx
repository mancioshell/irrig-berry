import React from 'react';

export default function Jumbotron() {
  return (<div className="jumbotron">
    <div className="container">

      <div className="row">
        <div className="col-2">
          <img src="img/waterberry.png" className="img-fluid" alt="..." />
        </div>
        <div className="col-10">
          <h1>WaterBerry</h1>
          <h4>Il tuo centro di irrigazione personalizzato </h4>
        </div>
      </div>
    </div>
  </div>)
}
