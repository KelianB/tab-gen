import React from 'react';
// import 'bootstrap/dist/css/bootstrap.css';

import { connect } from 'react-redux';
import { versionHasBeenSelected } from '../ReduxStuff/Actions'

import JobRetriever from './JobRetriever/JobRetriever'
import AudioRecorder from './AudioRecorder/AudioRecorder'
import FileUploader from './FileUploader/FileUploader'

import ToggleButton from '@material-ui/lab/ToggleButton';
import ToggleButtonGroup from '@material-ui/lab/ToggleButtonGroup';

import {BACK_URL, GET_VERSIONS_ROUTE} from '../../config.js'






class InfoInput extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            models: [],
            selectedModel: null,
            selectedInputMethod:0,
        }
    }


    // Version related methods

    versionURL = () => {
        return BACK_URL + GET_VERSIONS_ROUTE
    }

    handleVersion = (event, newModel) => {

        this.props.versionHasBeenSelected(newModel);
        this.setState({selectedModel: newModel}, () => console.log(this.state.selectedModel))
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
                                        <ToggleButton value = {model.id} >
                                            {model.name}
                                        </ToggleButton>

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
                    <FileUploader />
                }   

                {
                    selectedInputMethod == 1 &&
                    <div class="form-group">
                        <label className= "upload-title"> RECORD WITH YOUR MICROPHONE  </label>
                        <AudioRecorder />
                    </div>
                }

                <div class="form-group">
                    <JobRetriever />
                </div>

            </div>
        )
    }
}

export default connect(null, {versionHasBeenSelected})(InfoInput)
