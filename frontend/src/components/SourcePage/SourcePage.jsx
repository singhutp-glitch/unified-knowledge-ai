import React, { useState,useEffect } from 'react'
import "./SourcePage.css" 
import { getPickerToken,putRootFolderId,removeRootFolder
  ,getRootFolder,getCheckoutChanges, syncAllCheckoutChanges,
 getActiveSyncJob } from '../../services/sourceApi'
import { openGoogleDrivePicker } from '../../services/googleDriverPicker'
import SyncStatusPage from '../SyncStatusPage/SyncStatusPage'


const SourcePage = ({sourceInfo}) => {
  const [selectedTab,setSelectedTab] = useState("syncFolder")
  const [rootFolder,setRootFolder] = useState({});
  const [checkoutChanges,setCheckoutChanges] = useState("notUpdated");
  const [disableSyncAll,setDisableSyncAll] = useState(false);
  const [syncJob,setSyncJob] = useState(null);
  
  useEffect(() => {
        async function loadRootFolder() {
            const data = await getRootFolder();
            console.log("root folder - ",data);
            setRootFolder(data);
        }

        loadRootFolder();
    }, []);

    useEffect(() => {

    async function checkActiveSync() {

        try {
            const data = await getActiveSyncJob();

            if (data.active) {

                setSyncJob(data.job);
            }

        } catch (error) {
            console.error(
                "Failed to check active sync",
                error
            )
        }
    }

    checkActiveSync();

}, []);
    
  
async function handleSyncAll(){
  try{  
      const payload = {
        external_file_ids: checkoutChanges.map(
        change => change.file.id
    )
};
 setDisableSyncAll(true);
 const statusResponse = await syncAllCheckoutChanges(payload);
 setDisableSyncAll(false);
 setSyncJob(statusResponse);

  }catch(error){
    console.error(error);
  }

}

  async function handleCheckoutClick(){
    const result = await getCheckoutChanges();

    setCheckoutChanges(result.changes);
  }

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
      setRootFolder({});
    }catch(error){
      console.log(error);
    }
    
  }

  return (
  <div className="admin-source-page">
    <div className="admin-source-bar">
      <div className="admin-source-bar-tabs">
        {sourceInfo.name}
      </div>

      <div
        className="admin-source-bar-tabs"
        onClick={() => {
          setSelectedTab("syncFolder");
        }}
      >
        Sync Folder
      </div>

      <div
        className="admin-source-bar-tabs"
        onClick={() => {
          setSelectedTab("checkout");
        }}
      >
        Checkout
      </div>
      <div
        className="admin-source-bar-tabs"
        onClick={() => {
          setSelectedTab("syncStatus");
        }}
      >
        Sync Status
      </div>
    </div>

    <div className="admin-source-page-main">
      {selectedTab === "syncFolder" ? (
        <div className="sync-folder-page">
          sync-folder page

          <div className="sync-folder-items">
            <div className="sync-folder-message">
              Sync Folder:
            </div>

            {rootFolder.id ? (
              <>
                <div className="selected-folder">
                  {rootFolder.name}
                </div>

                <div className="folder-selection-buttons">
                  <button
                    className="folder-select"
                    onClick={handleSelectFolder}
                  >
                    Change root folder
                  </button>

                  <button
                    className="folder-remove"
                    onClick={handleRemoveFolder}
                  >
                    Remove root Folder
                  </button>
                </div>
              </>
            ) : (
              <>
                <div className="selected-folder">
                  No Folder Selected
                </div>

                <div className="folder-selection-buttons">
                  <button
                    className="folder-select"
                    onClick={handleSelectFolder}
                  >
                    Select a folder
                  </button>
                </div>
              </>
            )}
          </div>
        </div>
      ) : selectedTab === "checkout" ? (
        <div className="checkout-page">
          checkout page

          <br />

          <button
            onClick={handleCheckoutClick}
            className="checkout-button"
          >
            checkout
          </button>

          <div className="changes-text">
            changes:
            {typeof(checkoutChanges)=== "object" &&
            <button className="sync-all-button" onClick={handleSyncAll} 
            disabled={disableSyncAll}>
            sync all
          </button>}
          </div>

          <div className="changes">
            {checkoutChanges === "notUpdated"
              ? "not checked yet"
              : checkoutChanges.map((change) => (
                  <div
                    key={change.file.id}
                    className="change-item"
                  >
                    {change.type} - {change.file.name}
                  </div>
                ))}
          </div>
        </div>
      ) : (
        <SyncStatusPage syncJob={syncJob} setSyncJob={setSyncJob}/>
      )}
    </div>
  </div>
)
}

export default SourcePage