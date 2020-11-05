import { AlphaTab } from './alphatab-full'
import React from 'react'

class TabRenderer extends React.Component {
    render() {
        const setting = {
            file: "https://www.alphatab.net/files/canon.gp",
            tracks: [0]
        };

        return (
            <AlphaTab settings={setting} id="test" />
        )

    }
}

export { TabRenderer }
