/**
 * Actions definition
 */
const UPLOAD_IS_OVER = "UPLOAD_IS_OVER"
const PROCESSING_IS_OVER = "PROCESSING_IS_OVER"

const processingIsOverAction = score => {return {type:PROCESSING_IS_OVER, score:score} };
const uploadIsOverAction = job_id => {return {type:UPLOAD_IS_OVER, job_id:job_id}}

export {UPLOAD_IS_OVER,PROCESSING_IS_OVER, processingIsOverAction,uploadIsOverAction}
