import logo from './logo.svg';
import './App.css';
import React from 'react';
import axios from 'axios';

const URL = "http://localhost:8000/upload";
const MAX_SIZE = 4 * (10 ** 6); // Max size in bytes (?)

class FileUploader extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      selectedFile: null,
    }
  }


  onChangeHandler = event => {
    console.log(event.target.files[0]);
    if (this.checkMimeType(event) && this.checkFileSize(event)) {
      this.setState({
        selectedFile: event.target.files[0],
        loaded: 0,
      })
    }

  }

  checkMimeType = event => {
    let file = event.target.files[0]
    let err = '' // Error message container

    const types = ['audio/mp3', 'audio/wav', 'audio/mpeg', 'audio/x-wav']

    if (types.every(type => file.type !== type)) {
      err += file.type + ' is not a supported format \n'
    }

    if (err !== '') { // if there are erros
      event.target.value = null; // discard selected file
      console.log(err)
      return false
    }
    return true;
  }

  checkFileSize = event => {
    let file = event.target.files[0]
    let size = MAX_SIZE;
    let err = "";

    if (file.size > size) {
      err += file.name + " is too large. Uploaded files must be smaller than " + size / (10 ** 6) + " MB"
    }

    if (err !== '') {
      event.target.value = null
      console.log(err)
      return false
    }

    return true

  }




  onClickHandler = () => {
    const data = new FormData();
    data.append('file', this.state.selectedFile)

    axios.post(URL, data, {}).then(res => {
      console.log(res.statusText)
    })
  }


  render() {

    return (
      <div>
        <input type="file" name="file" onChange={this.onChangeHandler} />
        <button type="button" class="btn btn-success btn-block" onClick={this.onClickHandler}>Upload</button>
      </div>
    )

  }
}

class App extends React.Component {
  constructor(props) {
    super(props);
  }


  render() {



    return (

      <div className="App">
        <header className="App-header">
          <img src={logo} className="App-logo" alt="logo" />

          <FileUploader />

        </header>
      </div>
    )

  };
}

export default App;
