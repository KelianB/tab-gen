
// CONFIG FILE OF BACKEND API

const BACK_URL = 'projeta3.klethuillier.fr:8000'

const POST_FILE_UPLOAD_ROUTE = '/api/job'
const GET_VERSIONS_ROUTE  = '/api/versions'
// const GET_RESULTS = (job_id) => `/api/job/${job_id}/result` // Inutile car normalement donné par le back 

const WS_END_POINT = '/ws/api/job'
const WS_MSG_REQUEST_PROGRESS = 'request_progress'
const WS_MSG_CURRENT_PROGRESS = 'current_progress'


const UPLOAD_MAX_SIZE = 10 * (10 ** 6) // Max size of uploaded file in bytes


const DEBOUNCE_TIMEOUT = 1000 // Time between the response of the API and the next request to check on the processing state


export {BACK_URL, POST_FILE_UPLOAD_ROUTE, GET_VERSIONS_ROUTE, WS_END_POINT, WS_MSG_REQUEST_PROGRESS, WS_MSG_CURRENT_PROGRESS, UPLOAD_MAX_SIZE, DEBOUNCE_TIMEOUT}
