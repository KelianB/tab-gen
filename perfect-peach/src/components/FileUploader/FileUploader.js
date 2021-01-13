import React from 'react';
import axios from 'axios';
import { Progress } from 'reactstrap';
import { ToastContainer, toast } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';
import 'bootstrap/dist/css/bootstrap.css';

import { connect } from 'react-redux';
import { uploadIsOverAction,processingIsOverAction } from '../ReduxStuff/Actions'
import JobRetriever from './JobRetriever'
import AudioRecorder from '../AudioRecorder'

import ToggleButton from '@material-ui/lab/ToggleButton';
import ToggleButtonGroup from '@material-ui/lab/ToggleButtonGroup';
import ToolTip from '@material-ui/core/Tooltip'

import {BACK_URL, UPLOAD_MAX_SIZE, POST_FILE_UPLOAD_ROUTE, GET_VERSIONS_ROUTE} from '../../config.js'






class FileUploader extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            selectedFile: null,
            buttonDisabled: true,
            models: [],
            selectedModel: null,
            selectedInputMethod:0,
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
                buttonDisabled: (this.state.selectedModel != null) ? false : true,
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
        const params = {"version_id":this.state.selectedModel}

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

            
            this.addJobToLocalStorage(job_id);
            this.props.uploadIsOverAction(job_id);


        }).catch(err => {
            toast.error('upload fail')
            console.log("Upload Error : " + err.statusText)
        })




    }

    addJobToLocalStorage = job_id => {
        if (job_id) {
            let previousJobs = localStorage.getItem("jobs")
            if (previousJobs == null) {
                previousJobs = []
            } else {
                previousJobs = JSON.parse(previousJobs)
            }
            previousJobs.push(job_id)
            localStorage.setItem("jobs", JSON.stringify(previousJobs))
        } else {
            console.log("ERROR - Null Job ID")
        }
    }

    // Version related methods

    versionURL = () => {
        return BACK_URL + GET_VERSIONS_ROUTE
    }

    handleVersion = (event, newModel) => {
        this.setState({selectedModel: newModel, buttonDisabled:(this.state.selectedFile != null) ? false: true}, () => console.log(this.state.selectedModel))
    }

    getModelVersions = () => {

        fetch( this.versionURL() )
         .then(res => res.json())
         .then(models => {this.setState({models:models})})
    }

    // Input method related methods

    handleInputMethod = (event, newMethod) => {
        this.setState({selectedInputMethod: newMethod})
    }

    componentDidMount = () => {
        this.getModelVersions()
    }

    render() {
        const WrappedToolTip = (props,ref) => <ToolTip {...props} />;

        const { models,selectedInputMethod } = this.state;
        const inputMethods = [{name:"Upload", id:"0"}, {name:"Record", id:"1"}]


        return (


            <div class="container">

                <div class="form-group">
                    <label className= "upload-title"> SELECT THE MODEL </label>
                    <div>
                        <ToggleButtonGroup value = {this.state.selectedModel} exclusive onChange = {this.handleVersion} id="o" aria-label = "mdr"  >

                            { 
                                models.map((model) => 
                                // <WrappedToolTip title = {model.description} key = {model.id}>
                                        <ToggleButton value = {model.id} >
                                            {model.name}
                                        </ToggleButton>

                                    // </WrappedToolTip>
                                    )
                            }

                        </ToggleButtonGroup>
                    </div>
                </div>

                <div class="form-group">
                    <label className= "upload-title"> SELECT YOUR INPUT METHOD </label>
                    <div>
                        <ToggleButtonGroup value = {this.state.selectedInputMethod} exclusive onChange = {this.handleInputMethod} id="m" aria-label = "lol"  >

                            { 
                                inputMethods.map((method) => 
                                        <ToggleButton value = {method.id} >
                                            {method.name}
                                        </ToggleButton>
                                    )
                            }

                        </ToggleButtonGroup>
                    </div>
                </div>

                {
                    selectedInputMethod == 0 &&
                    <div>
                        <div class="form-group files">
                            <label className= "upload-title"> UPLOAD YOUR FILE </label>
                            <input type="file" name="file" onChange={this.onChangeHandler} />
                        </div>
                        
                        <div class="form-group">
                            <ToastContainer />
                            <Progress max="100" color="success" value={this.state.loaded} >{Math.round(this.state.loaded, 2)}%</Progress>
                        </div>

                        <button type="button" class="btn upload-button btn-block" disabled={this.state.buttonDisabled} onClick={this.onClickHandler}> UPLOAD </button>
                    </div>
                }

                {
                    selectedInputMethod == 1 &&
                    <div class="form-group">
                        <label className= "upload-title"> RECORD WITH YOUR MICROPHONE  </label>
                        <AudioRecorder/>
                    </div>
                }


                

                <div class="form-group">
                    <JobRetriever />
                </div>

            </div>
        )
    }
}

/*
 * This line connects FileUploader react component with the Store so
 * that FileUploader can dispatch action by using for instance
 * 'this.props.uploadIsOverAction'
 */
export default connect(null, {uploadIsOverAction,processingIsOverAction})(FileUploader)
