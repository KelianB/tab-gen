import {combineReducers} from 'redux';
import {UPLOAD_IS_OVER,PROCESSING_IS_OVER} from './Actions'

//Reducers definition


const initialState = {
    uploadDone: false, //Upload of file on the server that will compute tabs out of audio
    uploading: false,
    score_processing: false,
    score_processing_over:false,
    score:null,
}

const PeachReducer = (state = initialState, action) => {
    switch (action.type) {
        case UPLOAD_IS_OVER:
            console.log("ALED")
            return {...state, uploadDone:true, uploading:false, score_processing:true}

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
