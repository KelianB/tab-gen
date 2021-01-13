import React from 'react'
import axios from 'axios'
import RecorderJS from 'recorder-js'
import { Progress } from 'reactstrap';
import { getAudioStream, exportBuffer } from './utilities/audio'

import { connect } from 'react-redux';
import { uploadIsOverAction } from './ReduxStuff/Actions'

import {BACK_URL, POST_FILE_UPLOAD_ROUTE} from '../config.js'
const URL = BACK_URL + POST_FILE_UPLOAD_ROUTE;

class AudioRecorder extends React.Component {
    constructor(props) {
        super(props);

        this.state = {
            stream: null,
            recording: false,
            recorder: null,
            recorded: null,
            buttonDisabled:true,
            recorded_audio:null,
        }
    }

    async componentDidMount() {
        let stream;

        try {
            stream = await getAudioStream();

        } catch (error) {
            // Toast error TODO
            console.log(error)
        }

        this.setState({ stream });
    }

    startRecording() {
        const { stream } = this.state;
        const audioContext = new (window.AudioContext || window.webkitAudioContext)();
        const recorder = new RecorderJS(audioContext);
        recorder.init(stream)

        this.setState({
            recorder: recorder,
            recording: true,
        },
            () => recorder.start()
        );
    }

    async stopRecording() {

        const { recorder } = this.state;
        const { buffer } = await recorder.stop();
        const audio = exportBuffer(buffer[0]);

        this.setState({recorded_audio:audio, buttonDisabled:false, loaded:0})



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

    onUploadClickHandler = () => {
        
        const data = new FormData();
        const params = {"version_id": this.props.version_id}

        data.append('file', this.state.recorded_audio)


        axios.post(URL, data, {params:params}, {

            onUploadProgress: ProgressEvent => {
                this.setState({ loaded: (ProgressEvent.loaded / ProgressEvent.total * 100), 
            })}  
                 
        }).then(res => {
            console.log("Upload Status : " + res.statusText);
            this.setState({
                recording: false,
                recorder: true
            });
            console.log(res.data)

            const job_id = res.data.job_ws

            this.props.uploadIsOverAction(job_id);

        }).catch(err => {
            console.log("Upload Error : " + err.statusText)
        })

    }


    render() {

        const { recording, stream } = this.state;

        // Don't show record button if the browser doesn't support it
        if (!stream) {
            return null;
        }

        return (
            <div>

                <div class="form-group"> 
                    <button class="btn upload-button btn-block" disabled={this.state.recorded_audio != null} onClick={() => recording ? this.stopRecording() : this.startRecording()}>
                        {recording ? 'Stop Recording' : 'Start Recording'}
                    </button >  
                </div>


                <button type="button" class="btn upload-button btn-block" disabled={this.props.version_id == null || this.state.recorded_audio == null} onClick={this.onUploadClickHandler}> UPLOAD </button>

                {this.state.loaded > 0 &&
                    <div class="form-group">
                        <Progress max="100" color="success" value={this.state.loaded} >{Math.round(this.state.loaded, 2)}%</Progress>
                    </div>
                }
            </div>



        )
    }
}


/*
 * This line connects AudioRecorder react component with the Store so
 * that AudioRecorder can dispatch action by using for instance
 * 'this.props.uploadIsOverAction'
 */

const mapStateToProps =  store =>({
    version_id: store.peachReducer.version_id
  })

export default connect(mapStateToProps, {uploadIsOverAction})(AudioRecorder)
