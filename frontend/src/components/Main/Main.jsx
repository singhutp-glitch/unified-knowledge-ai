import React, { useEffect, useRef } from 'react'
import './Main.css'
import {assets} from '../../assets/assets.js'
import { useState } from 'react'
import { streamMessage } from '../../services/api.js'
import { createNewChatId } from '../../services/api.js'
import { uploadDocument } from '../../services/ragApi.js'
import { sendRetrievalQuery } from '../../services/ragApi.js'
import ChatContainer from '../ChatContainer/ChatContainer.jsx'
import Greet from '../Greet/Greet.jsx'


const Main = ({currentChatId,setCurrentChatId,loadChats,messages,setMessages
    ,user,setSourceBar, setSourceBarSources,documentSourceCache, setDocumentSourceCache}) => {
    const [prompt,setPrompt] = useState('');
    const messageViewportRef = useRef(null);
    const [showMenu,setShowMenu] = useState(false);
    const [selectedFile,setSelectedFile] = useState(null);
    const fileInputRef = useRef(null);
    const [knowledgeScope,setKnowledgeScope] = useState("chat");
    const [searchMode,setSearchMode] = useState(false);
    const [isUploading,setIsUploading] = useState(false);
    const [documentContent,setDocumentContent] = useState('');
    const [showContent, setShowContent] = useState(false);
    

    useEffect(() => {
    scrollMessagesToBottom("auto");
}, [messages]);

    
    const isSendDisabled = knowledgeScope === 'user'||
                           knowledgeScope === 'company'||
                           isUploading;
    const documentSearch = knowledgeScope !== 'nofile';

    function handleUploadClick() {

        fileInputRef.current.click();
    };
    async function handleUpload() {

    if (!selectedFile) return;

    const fileName = selectedFile.name;
     setMessages(prev => [
        ...prev,
        {
            role: "system",
            content: `Uploading ${fileName}...\n\nPlease wait , it may take about a minute`,
        }]);
        

            let chatId = currentChatId;
        if (chatId === null) {

            chatId = await createNewChatId(selectedFile.name);
            loadChats();

            setCurrentChatId(chatId);
        }

    try {
        setIsUploading(true);

        const uploadResponse = await uploadDocument(selectedFile,chatId);

        setSelectedFile(null);
        fileInputRef.current.value = "";
        setIsUploading(false);
          setMessages(prev => {

                    const updated = [...prev];

                    updated[
                        updated.length - 1
                    ] = {
                        ...updated[
                            updated.length - 1
                        ],
                        content: ` ${fileName}\nFile upload complete.`,
                        loading: false,
                    };

                    scrollMessagesToBottom("smooth");
                    return updated;
                });
                setDocumentContent(uploadResponse.documentContent);
        

    } catch (err) {

        console.error(err);
    }
}

    function handleFileChange(event) {

    const file = event.target.files[0];

    if (!file) return;

    setSelectedFile(file);

    setShowMenu(false);

}

    async function sendModelPrompt({currentPrompt}){
         setMessages(prev => [
        ...prev,
        {
            role: "user",
            content: currentPrompt,
        },
        {
            role: "assistant",
            content: "",
            loading: true,
            citations:[],
            status:'Thinking...',
        },
    ]);

        scrollMessagesToBottom("smooth");
    try {

        let chatId = currentChatId;

        if (chatId === null) {

            chatId =
                await createNewChatId(
                    currentPrompt
                );
            loadChats();

            setCurrentChatId(chatId);
        }
        let accumulated = "";

        await streamMessage(
            chatId,
            documentSearch,
            currentPrompt,
            chunk => {

                accumulated += chunk;

                setMessages(prev => {

                    const updated = [...prev];

                    updated[
                        updated.length - 1
                    ] = {
                        ...updated[
                            updated.length - 1
                        ],
                        content: accumulated,
                        loading: false,
                    };

                    scrollMessagesToBottom("smooth");
                    return updated;
                });
            },
            documentSources => {
                const newChunks = Object.values(documentSources).reduce((acc, chunk) => {
                        acc[chunk.id] = chunk;
                        return acc;
                    }, {});

                    setDocumentSourceCache(prev => ({
                        ...prev,
                        ...newChunks
                    }));
                const newCitations = Object.entries(documentSources).map(([cn, chunk]) => ({
                    citationNumber: Number(chunk.citationNumber),
                    chunkId: chunk.id
                }));

                setMessages(prev => {
                    const updated = [...prev];

                    updated[updated.length - 1] = {
                        ...updated[updated.length - 1],
                        citations:newCitations,
                        loading:true
                    };

                    return updated;
                });
            
            },
            status => {
                setMessages(prev => {

                    const updated = [...prev];

                    updated[updated.length - 1] = {
                        ...updated[updated.length - 1],
                        status
                    };

                    return updated;
                });
            
            },
            error=> {
                accumulated += error;
                setMessages(prev => {

                    const updated = [...prev];

                    updated[updated.length - 1] = {
                        ...updated[updated.length - 1],
                        content:accumulated,
                        loading:false

                    };

                    return updated;
                });
            
            }
        );
        

    } catch (error) {
        console.error(error);
    }
    }
    async function sendRetrievelQuery({retrievalQuery}){
         setMessages(prev => [
        ...prev,
        {
            role: "user",
            content: retrievalQuery,
        },
        {
            role: "assistant",
            content: "",
            documentSources:[],
            loading: true,
            status:'Retrieving...',
        },
    ]);

       scrollMessagesToBottom("smooth");
    try {

        let chatId = currentChatId;

        if (chatId === null) {

            chatId =
                await createNewChatId(
                    retrievalQuery
                );
            loadChats();

            setCurrentChatId(chatId);
        };
        const response = await sendRetrievalQuery(chatId,retrievalQuery);
        const textResponse = response.chunkResults.map((chunkResult,index)=>{
            return `
Result - ${index+1}
chunk id - ${chunkResult.chunkId}
File - ${chunkResult.originalFileName}
type - ${chunkResult.type}
score - ${chunkResult.score}
Section - ${chunkResult.sectionHeading}
${chunkResult.text}
            `
        })
        const textResults = textResponse.join("");
  
        setMessages(prev => {

                    const updated = [...prev];

                    updated[
                        updated.length - 1
                    ] = {
                        ...updated[
                            updated.length - 1
                        ],
                        content: textResults,
                        loading: false
                    };
                  
           scrollMessagesToBottom("smooth");
                    return updated;
                });
            

    } catch (error) {
        console.error(error);
    }
    }


    const handleSend = async () => {
        console.log('send');
    await handleUpload();
    if (!prompt.trim()) return;
    const userQuery = prompt;
    setPrompt("");
    if(searchMode){
        sendRetrievelQuery({retrievalQuery:userQuery});
    }
    else{
        sendModelPrompt({currentPrompt:userQuery});
    }
};

function scrollMessagesToBottom(behavior = "smooth") {
    if (!messageViewportRef.current) return;

    messageViewportRef.current.scrollTo({
        top: messageViewportRef.current.scrollHeight,
        behavior,
    });
}


  return <div className="main">

    <div className="message-viewport"    ref={messageViewportRef}> 
        <div className="main-container">
            {messages.length === 0 ? (
                <Greet user={user} />
            ) : (
                <ChatContainer
                    messages={messages}
                    setSourceBar={setSourceBar}
                    setSourceBarSources={setSourceBarSources}
                    documentSourceCache={documentSourceCache}
                    setDocumentSourceCache={setDocumentSourceCache}
                    showContent = {showContent}
                    documentContent = {documentContent}
                />
            )}
        </div>

    </div>

    <div className="composer">
       
            <div className="main-bottom">
                {selectedFile && (
                        <div className='selected-file'>
                            📄 {selectedFile.name}
                        </div>
                    )}
                {knowledgeScope === 'company' &&(
                    <div className='search-scope-message'>
                            No company knowledge connect
                        </div>)}
                  {knowledgeScope === 'user' &&(
                    <div className='search-scope-message'>
                            No user files connected
                        </div>)}
               {

                    showMenu && (

                    <div className="composer-toolbar">

                        <button 
                            onClick={handleUploadClick}
                            className={`toolbar-item ${isUploading?'uploading':''}`}
                            disabled={isUploading}
                        >
                            {isUploading?'Uploading...':'Upload File'}
                        </button>


                        <div className="toolbar-item">

                            <label>
                                Knowledge Scope
                            </label>

                            <select
                                value={knowledgeScope}
                                onChange={(e)=>setKnowledgeScope(e.target.value)}
                            >

                                <option value="chat">
                                     Chat Files
                                </option>

                                <option value="user">
                                    All User Files
                                </option>

                                <option value="company">
                                    Company Knowledge
                                </option>
                                <option value="nofile">
                                    No file
                                </option>

                            </select>

                        </div>


                        <button
                            className="toolbar-item"
                            onClick={()=>setSearchMode(prev=>!prev)}
                        >

                            {searchMode ? "Search Mode" : "Chat Mode"}

                        </button>


                        <button
                            className="toolbar-item"
                            onClick={()=>setShowContent(prev=>!prev)}
                        >

                            {"show content"}

                        </button>

                        

                    </div>

                    )
                    }
                   
                {!searchMode && (<>
                </>)}
                <div className="search-box">
                    <div >
                       <img
                            onClick={()=>setShowMenu(prev=>!prev)}
                            src={assets.plus_icon}
                            className="composer-plus"
                        />
                    </div>
                   
                    <input onChange={(e)=>{setPrompt(e.target.value)}} onKeyDown={(e) => {
        if (e.key === "Enter") {
            handleSend();
        }
    }}type="text" placeholder={
    searchMode
    ? "Search your knowledge..."
    : "Ask your documents..."
} value={prompt}/>
                    <button onClick={handleSend} disabled={isSendDisabled} 
                    className='send-button'>
                        <img  src={assets.send_icon} alt="" />
                    </button>
                </div>
            </div>
    </div>

    <input
        type="file"
        ref={fileInputRef}
        hidden
        onChange={handleFileChange}
    />

</div>
    }
export default Main