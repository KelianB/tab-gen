import {combineReducers, createStore} from 'redux';
import devToolsEnhancer from 'remote-redux-devtools';

/**
 * Actions definition
 */
const UPLOAD_IS_OVER = "UPLOAD_IS_OVER"
const PROCESSING_IS_OVER = "PROCESSING_IS_OVER"

const processingIsOverAction = score => {return {type:PROCESSING_IS_OVER, score:score} };
const uploadIsOverAction = () => {return {type:UPLOAD_IS_OVER}}

/**
 * Reducers definition
 */

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
            return {...state, uploadDone:true, uploading:false, tab_processing:true}

        case PROCESSING_IS_OVER:
            return {...state, tab_processing:false, score_processing_over: true, score: action.score}

        default:
            return state
    }
}

const Reducers = combineReducers({
    peachReducer: PeachReducer,
  });
  


/**
 * Store creation
 */

const Store = createStore(Reducers,window.__REDUX_DEVTOOLS_EXTENSION__ && window.__REDUX_DEVTOOLS_EXTENSION__());

export {Store, processingIsOverAction};
