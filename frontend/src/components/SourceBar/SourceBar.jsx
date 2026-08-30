import React from 'react'
import './SourceBar.css'
import SourceCard from "../SourceCard/SourceCard"

const SourceBar = ({startResize,sourceBarWidth,sourceBarSources,setSourceBar,
    setViewerOpen,setSelectedDocument    
}) => {

  return (
     <>
        <div
            className="source-resize-handle"
            onMouseDown={startResize}
        />

        <aside
            className="source-bar"
            style={{
                width:`${sourceBarWidth}px`
            }}
        >

        <div className="source-bar-header">

            <div>
                <h2>Sources</h2>
                <p>
                    {sourceBarSources.length} supporting passage
                    {sourceBarSources.length !== 1 ? "s" : ""}
                </p>
            </div>

            <button
                className="close-source-bar"
                onClick={() => setSourceBar(false)}
            >
                ✕
            </button>

        </div>

        <div className="source-bar-content">

            <div className="document-sources">

    {sourceBarSources.map((source, index) => (

        <SourceCard
            key={source.id ?? index}
            source={source}
            citationNumber={source.citationNumber}
            setViewerOpen={setViewerOpen}
            setSelectedDocument = {setSelectedDocument}
        />

    ))}

</div>

        </div>

    </aside>
     </>
  )
}

export default SourceBar