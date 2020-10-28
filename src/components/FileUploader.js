import React from 'react';
import axios from 'axios';
import { Progress, Button } from 'reactstrap';
import { ToastContainer, toast } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';
import 'bootstrap/dist/css/bootstrap.css';

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
            toast.error(err)
            return false
        }
        return true
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
            toast.error(err)
            console.log(err)
            return false
        }

        return true

    }

    onClickHandler = () => {
        const data = new FormData();
        data.append('file', this.state.selectedFile)

        axios.post(URL, data, {

            onUploadProgress: ProgressEvent => {
                this.setState({ loaded: (ProgressEvent.loaded / ProgressEvent.total * 100), })
            }

        }).then(res => {
            toast.success('upload success')
            console.log("Upload Status : " + res.statusText)
        }).catch(err => {
            toast.error('upload fail')
            console.log("Upload Error : " + err.statusText)
        })




    }

    render() {

        return (
            <div class="container">
                <div class="row">
                    <div class="offset-md-3 col-md-6">

                        <div class="form-group files">
                            <label> Upload your file </label>
                            <input type="file" name="file" onChange={this.onChangeHandler} />
                        </div>

                        <div class="form-group">
                            <ToastContainer />
                            <Progress max="100" color="success" value={this.state.loaded} >{Math.round(this.state.loaded, 2)}%</Progress>
                        </div>

                        <Button color="primary" onClick={this.onClickHandler}>Upload</Button>{''}


                    </div>
                </div>
            </div>
        )
    }
}


export { FileUploader }
