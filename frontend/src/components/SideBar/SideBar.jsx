import React, { useState } from 'react'
import './SideBar.css'
import {assets} from '../../assets/assets.js'
import { getMessages } from '../../services/api.js';
import UserProfile from '../UserProfile/UserProfile.jsx';
const SideBar = ({user,onLogout,chats,currentChatId,setCurrentChatId,setMessages}) => {
  const [extended,setExtended] = useState(false);
  const handleNewChat = ()=>{
    setCurrentChatId(null);
    setMessages([]);
  }
  const handleChatClick = async(chatId)=>{
    setCurrentChatId(chatId);
    const messages = await getMessages(chatId);
    setMessages(messages);
  }


  return (
  <div className={`side-bar ${extended ? "extended" : ""}`}>
      <div className='top'>
        <img onClick={()=>{setExtended(prev=>!prev)}} className="menu" src={assets.menu_icon} alt="" />
      <div onClick={handleNewChat} className='new-chat'>
        <img src={assets.plus_icon} alt="" />
        {extended?<p>New Chat</p>:null}
      </div>
      {extended?
      <div className="recent">
        <p className='recent-title'>Recent</p>
        {chats.map((chat) => (
          <div key = {chat.id} className={'recent-entry'+(chat.id===currentChatId?' current-chat':'')}
          onClick={()=>{handleChatClick(chat.id)}}>
          <img src={assets.message_icon} alt="" />
          <p>{chat.title.slice(0,15)}...</p>
        </div>
        ))}
        
      </div>
        :null}
      </div>
      <div className='bottom'>
        <div className="bottom-item recent-entry">
          <UserProfile user={user} onLogout={onLogout}/>
          {extended?<p className='bottom-user-name'>{user.name}</p>:null}
        </div>
      </div>
    </div>
  )
}

export default SideBar