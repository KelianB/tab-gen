import React from 'react';
import axios from 'axios';
import { processingIsOverAction } from '../ReduxStuff/Actions'
import { connect } from 'react-redux';
import socketIOClient from 'socket.io-client'
import {debounce} from 'lodash'
import { LinearProgress } from '@material-ui/core';
import './LoadingScreen.css'
//const sleep = require('util').promisify(setTimeout)


import {BACK_URL,WS_END_POINT, DEBOUNCE_TIMEOUT} from '../../config.js'


/**
 * L'idée de ce composant est d'afficher un écran de chargement pendant le traitement du fichier audio par le modèle
 * Pour vérifier l'état du traitement, le back est censé envoyer de manière 'régulière' un message 'current-status' sous forme de websocket contenant l'état actuel du traitement
 * Si le front n'a pas reçu de message depuis un certain temps TIMEOUT, le front envoie un message 'request-status' demandant au back l'état du traitement
 * A chaque message reçu par le back, le front retarde/debounce sa demande de status
 * Après reception du status 
 *          => Si le traitement est terminé (data.progress.done = true)
 *                  - on change l'état du composant en {tab_processing:false} => On change l'affichage du composant de loading à done
 *                  - on va récuperer le résultat (sendResultRequest)
 *                  - on dispatch l'action  processingIsOverAction au store, indiquant aux autres composants que le processing
 *                     est fini (ce qui permet d'activer/désactiver certains composant dans la class App) et ce qui fourni 
 *                     en même temps la partition
 *          
 *          => Si le traitement est encore en cours (this.data.etat = false)
 *                  - Il ne passe rien (à part un log qui confirme la réception)
 * 
 */


class LoadingScreen extends (React.Component) {
    constructor(props) {
        //Expected Props : job_id
        super(props)
        this.state = {
            tab_processing: true,
            is_over: false,
            result_url:null,
            steps: [],
            current_step: 1,
            progress : 0,
            step_progress: 0,

        }
    }

    sendResultRequest = async () => {

        console.log("LOADING - Sending request to get the result")
        const res = await axios.get(this.state.result_url)


        if (await res.data) {

            return this.props.processingIsOverAction(res.data) //res.data = partition/score
        } else {
            console("this shoudn't go there")
            return
        }
    }

    componentDidMount = () => {

        const socket = socketIOClient(BACK_URL + WS_END_POINT, {transports: ['websocket']});

        const requestProgress = () => socket.emit('request-progress', {job_id: this.props.job_id})
        const debounceEmission = debounce(requestProgress, DEBOUNCE_TIMEOUT )

        socket.on('current-status', (data) => {
            console.log("LOADING CURRENT STATUS RECEIVED : ")
            console.log(data)

            debounceEmission()

            if (data.progress.done === false) {
              
                console.log("LOADING - Processing is still going")
                this.setState({progress:data.progress.total_progress,steps:data.steps, current_step:data.progress.step, step_progress:data.progress.step_progress})


            
            } else {
                console.log("LOADING - Processing is over, the result has been received")
                this.setState({progress:data.progress.total_progress,steps:data.steps, current_step:data.progress.step, step_progress:data.progress.step_progress, tab_processing:false, is_over:true, result_url: data.result_url}, 
                  () => socket.disconnect())
            }
        });



    }


    render () {
        const progress = this.state.progress
        const current_step_progress = this.state.step_progress
        const steps = this.state.steps
        const current_step = this.state.current_step

        const step_progress = (step) => {
          if (step === steps[current_step - 1]) {return current_step_progress}
          else if (steps.indexOf(step) > current_step - 1) return 0
          return 1
        } 




            return(
                <div className="progress-container">
                    <div className="progress-bars">

                     <label className= "progress-title"> MAIN PROGRESS ({Math.round(progress*100)} %) </label>

                    <LinearProgress variant="determinate" value={progress*100} color="secondary" />


                      {steps.map( (step) => 
                      <div key={step} >
                        <label className= "progress-title"> {step} ({Math.round(step_progress(step)*100)} %) </label>

                        <LinearProgress variant="determinate" value={step_progress(step)*100} color="primary" />
                      </div>
                      )}
                    </div>
                    
                    <div className="progress-info">
                      <div className="progress-done">

                        <button type="button" className="btn upload-button btn-block" disabled={this.state.result_url === null} onClick={this.sendResultRequest}> RESULTS </button>


                      </div>
                    </div>


                    
                </div>
              )
        }
    
}



/*
 * This line connects LoadingScreen react component with the Store so
 * that LoadingScreen can dispatch action by using for instance
 * 'this.props.processingIsOverAction'
 */
export default connect(null, {processingIsOverAction})(LoadingScreen)
