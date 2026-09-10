import React from 'react'
import './AdminPage.css'
import { connectGoogleDrive, disconnectGoogleDrive } from '../../services/sourceApi.js'

const AdminPage = ({knowledgeSources,setKnowledgeSources}) => {

  const handleDisconnectGoogleDrive = async ()=>{
    try{
        await disconnectGoogleDrive();
        setKnowledgeSources([]);
    }catch(error){
        console.error(error);
    }
  }

  return (
    <div className="admin-page">
        <div className="sources-bar">
            <div className="source-tab">
                Sources
            </div>
        </div>
        <div className="sources-page">
            Sources:
            <div className="source-item">
                <div className="source-name">
                    Google drive
                </div>
                {knowledgeSources.length===0?
                    <><div className="source-connection">
                    Disconnected
                </div>
                <div className="source-buttons">
                    <button onClick={connectGoogleDrive} className="source-connect">
                        Connect
                    </button>
                </div></>
                : <><div className="source-connection">
                        Connected
                    </div>
                    <div className="source-buttons">
                        <button onClick={handleDisconnectGoogleDrive} className="source-disconnect">
                            Disconnect
                        </button>
                    </div></>
                }
            </div>
        </div>
    </div>
  )
}

export default AdminPage