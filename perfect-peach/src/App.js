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
        <div className="row fileupload">
          <div className="col"></div>
          <div className="col-6"> 
            <InfoInput />
          </div>
          <div className="col">  </div>
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
            <div className="header"> <img src={PPLogo} className="logo" alt="Perfect Peach Logo" /> </div>

            <div className="container main-content">

                <div className="separation" />
                
                  <this.transitionFull />
          
                <div className="separation" />


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
