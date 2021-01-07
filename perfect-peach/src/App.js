import './App.css';
import React, {useState, useEffect} from 'react';
import FileUploader from './components/FileUploader/FileUploader'
import './components/FileUploader/FileUploader.css'
import { TabRenderer } from './components/TabRenderer/TabRenderer'
import PPLogo from "./ressource/logo.svg"
import LoadingScreen from './components/LoadingScreen/LoadingScreen'

import { connect } from 'react-redux'





class App extends React.Component {
  constructor(props){
    super(props)
  };

  transitionFull = () => {

    if (this.props.upload_done == false) {
      return (        
        <div class="row fileupload">
          <div class="col"></div>
          <div class="col-6"> <FileUploader version_id = "0" /> </div>
          <div class="col">  </div>
        </div>
        )
    } else if (this.props.upload_done == true && this.props.score_processing == true && this.props.score_processing_over == false) {
          return (
          <LoadingScreen version_id = "0" job_id = "0"/>
          );
    } else if (this.props.score_processing == false &&  this.props.score_processing_over == true &&  (this.props.score != null)) {
          return (
          <TabRenderer full = {true} score = {this.props.score}/>
          );
    }


  }

  


  render() {
    
    
    
    return (
        <div>
            <div class="header"> <img src={PPLogo} class="logo" alt="Perfect Peach Logo" /> </div>

            <div class="container main-content">

                <div class="separation" />
                
                  <this.transitionFull />
          
                <div class="separation" />


            </div>
          </div>
      );

  }
}




const mapStateToProps =  store =>({
  score: store.peachReducer.score,
  uploading: store.peachReducer.uploading,
  upload_done: store.peachReducer.uploadDone,
  score_processing: store.peachReducer.score_processing,
  score_processing_over: store.peachReducer.score_processing_over

})


export default connect(mapStateToProps)(App)
