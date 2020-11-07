import AlphaTabFull from './AlphaTab/alphatab-full'
import AlphaTabLight from './AlphaTab/alphatab-light'
import React from 'react';

class TabRenderer extends React.Component {

    //<AlphaTabFull settings = {setting}/>
    //<AlphaTabLight tex={true} tracks ={[0]}> {alphatexString} </AlphaTabLight>
     
    render() {
        const setting = {
            file: "./static/files/canon.gp",
            tracks: [0]
        };


        return (
            <div>
                <AlphaTabFull settings = {setting}/>
            </div>


        )

    }
}

export { TabRenderer }
