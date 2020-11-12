import './App.css';
import React from 'react';
import FileUploader from './components/FileUploader/FileUploader'
import './components/FileUploader/FileUploader.css'
import { TabRenderer } from './components/TabRenderer/TabRenderer'
import PPLogo from "./ressource/logo.svg"

import { connect } from 'react-redux';



class App extends React.Component {

  


  render() {
    const partition2 = `\\title "Canon Rock" \\subtitle "JerryC" \\tempo 90 . :2 19.2{v f} 17.2{v f} | 15.2{v f} 14.2{v f}| 12.2{v f} 10.2{v f}| 12.2{v f} 14.2{v f}.4 :8 15.2 17.2 | 14.1.2 :8 17.2 15.1 14.1{h} 17.2 | 15.2{v d}.4 :16 17.2{h} 15.2 :8 14.2 14.1 17.1{b(0 4 4 0)}.4 | 15.1.8 :16 14.1{tu 3} 15.1{tu 3} 14.1{tu 3} :8 17.2 15.1 14.1 :16 12.1{tu 3} 14.1{tu 3} 12.1{tu 3} :8 15.2 14.2 | 12.2 14.3 12.3 15.2 :32 14.2{h} 15.2{h} 14.2{h} 15.2{h}14.2{h} 15.2{h}14.2{h} 15.2{h}14.2{h} 15.2{h}14.2{h} 15.2{h}14.2{h} 15.2{h}14.2{h} 15.2{h}`
    
    const partition = `\\title "Canon Rock"
    \\subtitle "JerryC"
    \\tempo 90
    .
    :2 19.2{v f} 17.2{v f} |
    15.2{v f} 14.2{v f}|
    12.2{v f} 10.2{v f}|
    12.2{v f} 14.2{v f}.4 :8 15.2 17.2 |
    14.1.2 :8 17.2 15.1 14.1{h} 17.2 |
    15.2{v d}.4 :16 17.2{h} 15.2 :8 14.2 14.1 17.1{b(0 4 4 0)}.4 |
    15.1.8 :16 14.1{tu 3} 15.1{tu 3} 14.1{tu 3} :8 17.2 15.1 14.1 :16 12.1{tu 3} 14.1{tu 3} 12.1{tu 3} :8 15.2 14.2 |
    12.2 14.3 12.3 15.2 :32 14.2{h} 15.2{h} 14.2{h} 15.2{h}14.2{h} 15.2{h}14.2{h} 15.2{h}14.2{h} 15.2{h}14.2{h} 15.2{h}14.2{h} 15.2{h}14.2{h} 15.2{h}
    `
    
    return (
        <div>
            <div class="header"> <img src={PPLogo} class="logo" alt="Perfect Peach Logo" /> </div>

            <div class="container main-content">

                <div class="separation" />

                {
                  //
                  //<TabRenderer score = {partition} />
                }

                
                  <Test1 score = {this.props.score}/>
          
                <div class="separation" />


            </div>
          </div>
      );

  }
}

function Test1(props) {

  if (props.score) {
      return (
                <TabRenderer full = {true} score = {props.score}/>

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


const mapStateToProps =  store =>({
  score: store.peachReducer.score
})

export default connect(mapStateToProps)(App)
