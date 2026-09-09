import React from 'react'
import './AdminPage.css'

const AdminPage = () => {
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
                <div className="source-connection">
                    Unconnected
                </div>
                <div className="source-buttons">
                    <button className="source-connect">
                        Connect
                    </button>
            </div>
            </div>
        </div>
    </div>
  )
}

export default AdminPage