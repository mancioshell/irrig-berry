import React from 'react';
import ReactDOM from 'react-dom';

import { HashRouter as BrowserRouter , Route, Switch, Redirect } from 'react-router-dom';

import 'bootstrap/dist/css/bootstrap.css';
import 'bootstrap/dist/js/bootstrap.js';
import 'cssDir/app.css';

import Nav from './nav'
import Jumbotron from './jumbotron'
import ElectrovalveViewer from './electrovalve-viewer'
import ElectrovalveList from './electrovalve-list'
import Configuration from './configuration'

class App extends React.Component {

  render() {

    return (<div id="parent">
      <div id="layout">
        <Nav></Nav>
        <Jumbotron></Jumbotron>
      </div>
      <div id="container" className="container-fluid">

        <Switch>
          <Route path='/electrovalves' component={ElectrovalveList}/>
          <Route path='/configure' component={Configuration}/>
          <Redirect to="/electrovalves" component={ElectrovalveList} />
        </Switch>

        <footer>
          <p>© Company 2017</p>
        </footer>
      </div>
    </div>);
  }
}

ReactDOM.render((
  <BrowserRouter>
    <App/>
  </BrowserRouter>
), document.getElementById('root'))
