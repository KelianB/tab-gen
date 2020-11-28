import React from 'react';
import axios from 'axios';
import { processingIsOverAction } from '../ReduxStuff/Actions'
import { connect } from 'react-redux';
import { toast } from 'react-toastify';


const sleep = require('util').promisify(setTimeout)

const TIMEOUT = 3000 // Time between the response of the API and the next request to check on the processing state
const URL = "http://localhost:8000"

/**
 * L'idée de ce composant est d'afficher un écran de chargement pendant le traitement du fichier audio par le modèle
 * Pour vérifier l'état du traitement on envoie en boucle une requête au back
 *          => Si le traitement est terminé (this.data.etat = true)
 *                  - on change l'état du composant en {tab_processing:false} => On change l'affiche du composant de loading à done
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
        this.state = {tab_processing: true}
    }




    stateURL = () => {
        return URL + `/api/version/${this.props.version_id}/${this.props.job_id}/state`
    }

    resultURL = () => {
        return URL + `/api/version/${this.props.version_id}/${this.props.job_id}/result`
    }

    // Envoie des requêtes en boucle jusqu'à ce que le traitement soit fini
    sendStateRequest = async () => {
        
        console.log("LOADING - Sending request to check processing status" )
        const res = await axios.get(this.stateURL())

        if (await res.data.etat == false) {

            console.log("LOADING - Processing is still going => Waiting " + TIMEOUT + " ms and retrying")
            return setTimeout(this.sendStateRequest, TIMEOUT);
        } else {
            
            console.log("LOADING - Processing is over : End of loading")
            this.setState({tab_processing:false})
            return await this.sendResultRequest()
        }

        


    }

    sendResultRequest = async () => {

        console.log("LOADING - Sending request to get the result")
        const res = await axios.get(this.resultURL())


        if (await res.data) {
            return this.props.processingIsOverAction(res.data)
        } else {
            return
        }
    }


    componentDidMount = () => {

        if (this.state.tab_processing == true) {
            this.sendStateRequest()
        }

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
