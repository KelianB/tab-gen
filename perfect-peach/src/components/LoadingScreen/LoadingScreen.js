import React from 'react';
import axios from 'axios';
import { processingIsOverAction } from '../ReduxStuff/Actions'
import { connect } from 'react-redux';
import { toast } from 'react-toastify';
import socketIOClient from 'socket.io-client'
const sleep = require('util').promisify(setTimeout)

const TIMEOUT = 2000 // Time between the response of the API and the next request to check on the processing state
const URL = "http://localhost:8000"
const SOCKET_ENDPOINT = "/api/job"

/**
 * L'idée de ce composant est d'afficher un écran de chargement pendant le traitement du fichier audio par le modèle
 * Pour vérifier l'état du traitement on envoie en boucle une requête au back
 *          => Si le traitement est terminé (this.data.etat = true)
 *                  - on change l'état du composant en {tab_processing:false} => On change l'affichage du composant de loading à done
 *                  - on va récuperer le résultat (sendResultRequest)
 *                  - on dispatch l'action  processingIsOverAction au store, indiquant aux composants que le processing
 *                     est fini (ce qui permet d'activer/désactiver certains composant dans la class App) et ce qui fourni 
 *                     en même temps la partition
 *          
 *          => Si le traitement est encore en cours (this.data.etat = false)
 *                  - On attend un certain temps TIMEOUT
 *                  - On renvoie une requête à l'API etc
 * 
 */


class LoadingScreen extends (React.Component) {
    constructor(props) {
        //Expected Props : job_id, version_id
        super(props)
        this.state = {
            tab_processing: true,
            is_over: false,
            result_url:null,
        }
    }

    sendResultRequest = async () => {

        console.log("LOADING - Sending request to get the result")
        const res = await axios.get(this.state.result_url)


        if (await res.data) {

            return this.props.processingIsOverAction(res.data) //res.data = partition/score
        } else {
            return
        }
    }

    componentDidMount = async () => {

        const socket = socketIOClient(URL + SOCKET_ENDPOINT, {transports: ['websocket']});

        socket.emit('request-progress', {job_id: this.props.job_id})

        socket.on('current-status', async (data) => {
            console.log("LOADING CURRENT STATUS RECEIVED : ")
            console.log(data)

            if (data.progress.done == false) {
                console.log("LOADING - Processing is still going => Waiting " + TIMEOUT + " ms and retryin")
                return setTimeout(() => socket.emit('request-progress', {job_id: this.props.job_id}), TIMEOUT);
            } else {
                this.setState({...this.state, tab_processing:false, is_over:true, result_url: data.result_url})
                socket.disconnect()
                return await this.sendResultRequest()
            }
        });
    }

    render () {

        if (this.state.tab_processing) {
            return (<div>Loading</div>)
        } else {
            return (
                    <div>Done</div>
            )
        }
    }
}



/*
 * This line connects LoadingScreen react component with the Store so
 * that LoadingScreen can dispatch action by using for instance
 * 'this.props.processingIsOverAction'
 */
export default connect(null, {processingIsOverAction})(LoadingScreen)
