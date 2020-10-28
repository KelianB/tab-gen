import logo from './logo.svg';
import './App.css';
import React from 'react';
import axios from 'axios';

const URL = "http://localhost:8000/upload";

class FileUploader extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      selectedFile: null,
    }
  }

  onChangeHandler = event => {
    console.log(event.target.files[0]);
    this.setState({
      selectedFile: event.target.files[0],
      loaded: 0,
    })
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
