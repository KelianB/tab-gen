import React from 'react';
import axios from 'axios';
import { Progress } from 'reactstrap';
import { ToastContainer, toast } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';
//import 'bootstrap/dist/css/bootstrap.css';

import { connect } from 'react-redux';
import { uploadIsOverAction } from '../../ReduxStuff/Actions'

import {BACK_URL, UPLOAD_MAX_SIZE, POST_FILE_UPLOAD_ROUTE} from '../../../config.js'






class FileUploader extends React.Component {
    // Expected props version_id given through the Store
    constructor(props) {
        super(props);
        this.state = {
            selectedFile: null,
            loaded: null,
        }
    }
    // Upload related methods

    uploadURL = () => {
        return BACK_URL + POST_FILE_UPLOAD_ROUTE
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
        let size = UPLOAD_MAX_SIZE;
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
        const params = {"version_id":this.props.version_id}

        data.append('file', this.state.selectedFile)


        console.log(this.state.selectedFile);

        axios.post(this.uploadURL(), data, {params:params}, {

            onUploadProgress: ProgressEvent => {
                this.setState({ loaded: (ProgressEvent.loaded / ProgressEvent.total * 100), })
            }

        }).then(res => {
            toast.success('upload success')
            console.log("Upload Status : " + res.statusText)

            console.log(res.data)

            const job_id = res.data.job_ws

            
            this.props.uploadIsOverAction(job_id);


        }).catch(err => {
            toast.error('upload fail')
            console.log("Upload Error : " + err.statusText)
        })




    }

    render() {


        return (

            <div>
                <ToastContainer />

                <div class="form-group files">
                    <label className= "upload-title"> UPLOAD YOUR FILE </label>
                    <input type="file" name="file" onChange={this.onChangeHandler} />
                </div>


                <div class="form-group"> 
                    <button type="button" class="btn upload-button btn-block" disabled={this.props.version_id == null || this.state.selectedFile == null} onClick={this.onClickHandler}> UPLOAD </button>
                </div>

                { this.state.loaded > 0 &&
                <div class="form-group">
                    <Progress max="100" color="success" value={this.state.loaded} >{Math.round(this.state.loaded, 2)}%</Progress>
                </div>
                }

                </div>
        )
    }
}

/*
 * This line connects FileUploader react component with the Store so
 * that FileUploader can dispatch action by using for instance
 * 'this.props.uploadIsOverAction'
 */

const mapStateToProps =  store =>({
    version_id: store.peachReducer.version_id
  })

export default connect(mapStateToProps, {uploadIsOverAction})(FileUploader)
