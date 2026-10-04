import React, { useState } from 'react'
import "./SourcePage.css" 

const SourcePage = ({sourceInfo}) => {
  const [selectedTab,setSelectedTab] = useState("syncFolder")


  return (
    <div className='admin-source-page'>
      <div className="admin-source-bar">
        <div className="admin-source-bar-tabs">
          {sourceInfo.name}
        </div>
        <div className="admin-source-bar-tabs">
          Sync Folder
        </div>
      </div>
      <div className="admin-source-page-main">
        {
          selectedTab==='syncFolder'?
          <div className="sync-folder-page">
            sync-folder page
            <div className="sync-folder-items">
                <div className="sync-folder-message">
                    Sync Folder:
                </div>
                {true?
                    <><div className="selected-folder">
                    No Folder Selected
                </div>
                <div className="folder-selection-buttons">
                    <button  className="folder-select">
                        Select a folder
                    </button>
                </div></>
                : <>
                {/* <div className="admin-source-connection">
                        Connected
                    </div>
                    <div className="admin-source-buttons">
                        <button onClick={handleDisconnectGoogleDrive} className="source-disconnect">
                            Disconnect
                        </button>
                    </div> */}
                    </>
                }
            </div>
          </div>:
          <div className="sync-status-page">
            sync status page
          </div>
        }
      </div>
    </div>
  )
}

export default SourcePage