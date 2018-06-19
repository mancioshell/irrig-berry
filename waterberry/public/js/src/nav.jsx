import React from 'react';

import {Link} from "react-router-dom";

export default function Nav() {
  return (<nav className="navbar navbar-expand-md navbar-dark fixed-top bg-dark">
    <a className="navbar-brand" href="#">WaterBerry</a>
    <button className="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarsExampleDefault" aria-controls="navbarsExampleDefault" aria-expanded="false" aria-label="Toggle navigation">
      <span className="navbar-toggler-icon"></span>
    </button>

    <div className="collapse navbar-collapse" id="navbarsExampleDefault">
      <ul className="navbar-nav mr-auto">
        <li className="nav-item active">
          <Link className="nav-link" to="/electrovalves">Elettrovalvole</Link>
        </li>
        <li className="nav-item">
          <Link className="nav-link" to="/configure">Configura</Link>
        </li>
      </ul>
      </div>
    </nav>);
}
