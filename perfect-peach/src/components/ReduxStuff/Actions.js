import { VERSION } from "lodash"

/**
 * Actions definition
 */
const VERSION_SELECTED = "VERSION_SELECTED"
const UPLOAD_IS_OVER = "UPLOAD_IS_OVER"
const PROCESSING_IS_OVER = "PROCESSING_IS_OVER"

const versionHasBeenSelected = version_id => {return {type:VERSION_SELECTED, version_id:version_id}}
const processingIsOverAction = score => {return {type:PROCESSING_IS_OVER, score:score} };
const uploadIsOverAction = job_id => {return {type:UPLOAD_IS_OVER, job_id:job_id}}

export {UPLOAD_IS_OVER,PROCESSING_IS_OVER, VERSION_SELECTED, processingIsOverAction,uploadIsOverAction,versionHasBeenSelected}
