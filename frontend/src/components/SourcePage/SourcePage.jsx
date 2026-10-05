import React, { useState } from 'react'
import "./SourcePage.css" 
import { getPickerToken,putRootFolderId } from '../../services/sourceApi'
import { openGoogleDrivePicker } from '../../services/googleDriverPicker'


const SourcePage = ({sourceInfo}) => {
  const [selectedTab,setSelectedTab] = useState("syncFolder")
  const [selectedFolder,setSelectedFolder] = useState(null);

  async function handleFolderSelected(folder) {

    console.log("Selected folder:", folder);

    // folder.id
    // folder.name
    const data = await putRootFolderId(folder.id);

    // Backend gives authoritative folder details
    setSelectedFolder(data.folder);
}
  const handleSelectFolder = async ()=>{
    try{
      const data = await getPickerToken();

      await openGoogleDrivePicker(data.access_token,handleFolderSelected);

    }catch(error){
      console.log(error);
    }
    
  }

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
                {selectedFolder?
                   <><div className="selected-folder">
                    {selectedFolder.name}
                </div>
                <div className="folder-selection-buttons">
                    <button  className="folder-select"
                    >
                        Change root folder
                    </button>
                </div></>
                    :
                      <><div className="selected-folder">
                    No Folder Selected
                </div>
                <div className="folder-selection-buttons">
                    <button  className="folder-select"
                    onClick={handleSelectFolder}>
                        Select a folder
                    </button>
                </div></>
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