import './App.css';
import React from 'react';
import { FileUploader } from './components/FileUploader/FileUploader'
import './components/FileUploader/FileUploader.css'
import { TabRenderer } from './components/TabRenderer/TabRenderer'

import PPLogo from "./ressource/logo.svg"



class App extends React.Component {

  render() {



    return (

      <div>
        
        <div class="header"> <img src={PPLogo} class="logo" alt="Perfect Peach Logo" /> </div>

        <div class="container main-content">


          <div class="row fileupload">
            <div class="col"></div>
            <div class="col-6"> <FileUploader /> </div>
            <div class="col">  </div>
          </div>

          <div class="row audiostream">
            <div class="col"></div>
            <div class="col-6"> <TabRenderer /> </div>
            <div class="col">  </div>
          </div>

        </div>
        </div>






    )

  };
}

export default App;
