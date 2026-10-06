import React, { useState,useEffect } from 'react'
import "./SourcePage.css" 
import { getPickerToken,putRootFolderId,removeRootFolder
  ,getRootFolder
 } from '../../services/sourceApi'
import { openGoogleDrivePicker } from '../../services/googleDriverPicker'


const SourcePage = ({sourceInfo}) => {
  const [selectedTab,setSelectedTab] = useState("syncFolder")
  const [rootFolder,setRootFolder] = useState(null);

   useEffect(() => {
        async function loadRootFolder() {
            const data = await getRootFolder();
            setRootFolder(data);
        }

        loadRootFolder();
    }, []);

  async function handleFolderSelected(folder) {

    console.log("Selected folder:", folder);

    // folder.id
    // folder.name
    const data = await putRootFolderId(folder.id);

    // Backend gives authoritative folder details
    setRootFolder(data.folder);
}
  const handleSelectFolder = async ()=>{
    try{
      const data = await getPickerToken();

      await openGoogleDrivePicker(data.access_token,handleFolderSelected);

    }catch(error){
      console.log(error);
    }
    
  }

  const handleRemoveFolder =async ()=>{
     try{
      await removeRootFolder();
      setRootFolder(null);
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
                {rootFolder?
                   <><div className="selected-folder">
                    {rootFolder.name}
                </div>
                <div className="folder-selection-buttons">
                    <button  className="folder-select"
                    >
                        Change root folder
                    </button>
                    <button  className="folder-remove"
                    onClick={handleRemoveFolder}
                    >
                        Remove root Folder
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