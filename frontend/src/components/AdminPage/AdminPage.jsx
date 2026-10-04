import React, { useState } from 'react'
import './AdminPage.css'
import { connectGoogleDrive, disconnectGoogleDrive } from '../../services/sourceApi.js'
import SourcePage from '../SourcePage/SourcePage.jsx'

const AdminPage = ({knowledgeSources,setKnowledgeSources}) => {

  const [selectedKnowledgeSource,setSelectedKnowledgeSource] = useState(null);
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
        <div className="admin-sources-bar">
            <div className="admin-source-tab" onClick={()=>{
                        setSelectedKnowledgeSource(null)}}>
                Sources:
            </div>
            {
                knowledgeSources.map((source,index)=>(
                <div className="admin-source-tabs" key={source.id}
                    onClick={()=>{
                        setSelectedKnowledgeSource(index)}}
                    >
                {source.name}
            </div>))
            }
        </div>
        {
            selectedKnowledgeSource!==null?
            <SourcePage sourceInfo={knowledgeSources[selectedKnowledgeSource]}/>:
            <div className="admin-sources-page">
            Sources:
            <div className="admin-source-item">
                <div className="admin-source-name">
                    Google drive
                </div>
                {knowledgeSources.length===0?
                    <><div className="admin-source-connection">
                    Disconnected
                </div>
                <div className="admin-source-buttons">
                    <button onClick={connectGoogleDrive} className="source-connect">
                        Connect
                    </button>
                </div></>
                : <><div className="admin-source-connection">
                        Connected
                    </div>
                    <div className="admin-source-buttons">
                        <button onClick={handleDisconnectGoogleDrive} className="source-disconnect">
                            Disconnect
                        </button>
                    </div></>
                }
            </div>
        </div>
        }
        
    </div>
  )
}

export default AdminPage