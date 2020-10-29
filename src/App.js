//import './App.css';
import React from 'react';
import { FileUploader } from './components/FileUploader'
import './components/style.css';
import './style.css'
import PPLogo from "./ressource/logo.svg"


class App extends React.Component {

  render() {



    return (


      <div class="wrapper">
        <div class="header"> <img src={PPLogo} class="logo" alt="Perfect Peach Logo" /></div>

        <div class="container main-content">

          <div class="row audiostream">
            <div class="col"></div>
            <div class="col-6"> <FileUploader /> </div>
            <div class="col">  </div>
          </div>



          <div class="row fileupload">
            <div class="col"></div>
            <div class="col-6"> <FileUploader /> </div>
            <div class="col">  </div>
          </div>

        </div>

      </div>
    )

  };
}

export default App;
