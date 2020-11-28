import './App.css';
import React from 'react';
import FileUploader from './components/FileUploader/FileUploader'
import './components/FileUploader/FileUploader.css'
import { TabRenderer } from './components/TabRenderer/TabRenderer'
import PPLogo from "./ressource/logo.svg"
import LoadingScreen from './components/LoadingScreen/LoadingScreen'

import { connect } from 'react-redux';



class App extends React.Component {
  constructor(props){super(props)}

  transition = () =>  {

    console.log(this.props)

    if (this.props.score) {
        return (
                  <TabRenderer full = {true} score = {this.props.score}/>
  
        )
    } else {
        return (        
                <div class="row fileupload">
                  <div class="col"></div>
                  <div class="col-6"> <FileUploader /> </div>
                  <div class="col">  </div>
                </div>
                )
    }
  }

  transitionLoading = () => {

    return (<LoadingScreen version_id = "0" job_id = "0"/>)
  }

  


  render() {
    
    
    
    return (
        <div>
            <div class="header"> <img src={PPLogo} class="logo" alt="Perfect Peach Logo" /> </div>

            <div class="container main-content">

                <div class="separation" />
                
                  <this.transitionLoading />
          
                <div class="separation" />


            </div>
          </div>
      );

  }
}




const mapStateToProps =  store =>({
  score: store.peachReducer.score
})

export default connect(mapStateToProps)(App)
