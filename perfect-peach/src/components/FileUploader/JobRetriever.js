import React from 'react'
import { connect } from 'react-redux';
import { uploadIsOverAction } from '../ReduxStuff/Actions'


class JobRetriever extends React.Component {
    constructor(props){
        super(props);
        this.state = {
            jobs:[]
        }
    }

    componentDidMount = () => {
        
        let previousJobs = localStorage.getItem("jobs")
        if (previousJobs == null) {
            previousJobs = []
        } else {
            previousJobs = JSON.parse(previousJobs)
        }
        this.setState({jobs:previousJobs})

    }

    onClickHandler = (job_id) => {
        if (this.state.jobs.length != 0) {
            this.props.uploadIsOverAction(job_id)
        }
    }

    render() {
        const jobs = this.state.jobs
        
        if (jobs.length != 0) {

            return (
                
                <div>
                    <div className = "separation"/>
                    <label className= "upload-title"> PREVIOUS SCORES </label>

                    {jobs.map((job_id => {
                        return <button type="button" class="btn upload-button btn-block" onClick={() => this.onClickHandler(job_id)}> Show Job {job_id} Status </button>
                    }))}
                </div>)
        } else {
            return (<div></div>)
        }


    }


}



/*
 * This line connects JobRetriever react component with the Store so
 * that JobRetriever can dispatch action by using for instance
 * 'this.props.uploadIsOverAction'
 */
export default connect(null, {uploadIsOverAction})(JobRetriever)
