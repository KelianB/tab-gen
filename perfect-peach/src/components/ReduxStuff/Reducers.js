import {combineReducers} from 'redux';
import {UPLOAD_IS_OVER,PROCESSING_IS_OVER, VERSION_SELECTED} from './Actions'

//Reducers definition


const initialState = {
    uploadDone: false, //Upload of file on the server that will compute tabs out of audio
    uploading: false,
    score_processing: false,
    score_processing_over:false,
    score:null,
    version_id:null,
}

const addJobToLocalStorage = job_id => {
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

const PeachReducer = (state = initialState, action) => {
    switch (action.type) {

        case VERSION_SELECTED:
            return {...state, version_id:action.version_id}
        
        case UPLOAD_IS_OVER:

            addJobToLocalStorage(action.job_id)
            return {...state, uploadDone:true, uploading:false, score_processing:true, job_id: action.job_id}

        case PROCESSING_IS_OVER:
            return {...state, score_processing:false, score_processing_over: true, score: action.score}

        default:
            return state
    }
}

const Reducers = combineReducers({
    peachReducer: PeachReducer,
  });

export default Reducers
