import {createStore} from 'redux';
import Reducers from './Reducers'

/**
 * Store creation
 */

 const Store = createStore(Reducers,window.__REDUX_DEVTOOLS_EXTENSION__ && window.__REDUX_DEVTOOLS_EXTENSION__());

export default Store
