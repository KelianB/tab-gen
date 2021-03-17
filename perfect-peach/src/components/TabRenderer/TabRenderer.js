import AlphaTabFull from './AlphaTab/alphatab-full'
import AlphaTabLight from './AlphaTab/alphatab-light'
import React from 'react';

class TabRenderer extends React.Component {

    //<AlphaTabFull settings = {setting}/>
    //<AlphaTabLight tex={true} tracks ={[0]}> {alphatexString} </AlphaTabLight>
     
    render() {
        // const setting = {
        //     file: "./static/files/canon.gp",
        //     tracks: [0]
        // };

        if (this.props.full === true) {
            return (
                <div>
                    <AlphaTabFull settings= {{tex:true}} > {this.props.score} </AlphaTabFull>
                    
                </div>
            )
        }
        else {
                <div>
                    <AlphaTabLight tex={true} tracks ={[0]}> {this.props.score} </AlphaTabLight>
                </div>
        }






    }
}

export { TabRenderer }
