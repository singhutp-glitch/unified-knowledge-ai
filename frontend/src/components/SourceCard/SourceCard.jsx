import React, { useState } from "react";
import "./SourceCard.css";

const SourceCard = ({ source, citationNumber,setSelectedDocument,setViewerOpen }) => {
    const [showFullChunk,setShowFullChunk] = useState(false);

  function handleViewDocument(document) {
    setSelectedDocument(document);
    setViewerOpen(true);
}


    return (
        <div className="source-card">

            <div className="source-card-header">

                <span className="citation-badge">
                    {citationNumber}
                </span>

                <span className="source-label">
                    Source
                </span>

            </div>

            <div className="source-document">

                {source.originalFileName}

            </div>


            <div className="source-metadata">

                Page {source.pages[0]}
                {source.pages[0]!==source.pages.at(-1) && ` - ${source.pages.at(-1)}`}

            </div>


            <div className="source-evidence">


                {showFullChunk?
                <span>{source.text.slice(0,1000)} <span className='more' onClick={()=>{setShowFullChunk(false)}}>  less</span></span> :
                <span>{source.text.slice(0,200)} <span className='less' onClick={()=>{setShowFullChunk(true)}}>  more</span></span>}

            </div>


            <button onClick={handleViewDocument} className="source-action">

                View document →

            </button>


        </div>
    );
};




export default SourceCard;