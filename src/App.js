//import './App.css';
import React from 'react';
import { FileUploader } from './components/FileUploader/FileUploader'
import './components/FileUploader/FileUploader.css'
import { TabRenderer } from './components/TabRenderer/TabRenderer'
import './style.css'

//import './components/TabRenderer.css'
import PPLogo from "./ressource/logo.svg"



class App extends React.Component {
/*
  componentDidMount () {
    const script = document.createElement("script");
    script.src = "/js/alphaTab/alphaTab.js";
    script.type = "text/javascript"

    document.head.appendChild(script);
}
*/

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
            <div class="col-6"> <FileUploader /> </div>
            <div class="col">  </div>
          </div>

        </div>
        </div>






    )

  };
}

export default App;
