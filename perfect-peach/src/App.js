import './App.css';
import React from 'react';
import './components/InfoInput/FileUploader/FileUploader.css'
import InfoInput from './components/InfoInput/InfoInput'
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
          <div class="col-6"> 
            <InfoInput />
          </div>
          <div class="col">  </div>
        </div>
        )
    } else if (this.props.upload_done == true && this.props.score_processing == true && this.props.score_processing_over == false && this.props.job_id != null) {
          return (
          <LoadingScreen job_id = {this.props.job_id}/>
          );
    } else if (this.props.score_processing == false &&  this.props.score_processing_over == true &&  (this.props.score != null)) {

          return (
          <TabRenderer full = {true} score = {this.props.score}/>
          );

          
    } else {
          return (<div>something went wrong :'( </div>)
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
  score_processing_over: store.peachReducer.score_processing_over,
  job_id: store.peachReducer.job_id
})


export default connect(mapStateToProps)(App)
