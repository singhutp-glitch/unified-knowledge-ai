import React, { useState } from 'react'
import './UserProfile.css'
const UserProfile = ({user,onLogout}) => {
    const [showMenu, setShowMenu] = useState(false);
    const initials = user.name.split(' ')
                        .map(word=>word[0])
                        .join('')
                        .slice(0,2)
                        .toUpperCase();

  return (
    <div onClick={()=>{setShowMenu(prev=> !prev)}} className="profile-container">
        <button className="user-avatar">{initials}</button>
         {showMenu && (
        <div className="profile-menu">
          <p>{user.name}</p>
          <p>{user.email}</p>

          <button onClick={onLogout}>
            Logout
          </button>
        </div>
      )}
    </div>
  )
}

export default UserProfile