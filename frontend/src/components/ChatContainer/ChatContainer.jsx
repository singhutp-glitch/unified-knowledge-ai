import { assets } from '../../assets/assets'
import './ChatContainer.css'
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import rehypeRaw from "rehype-raw";
import Citation from '../Citation/Citation';
import { preprocessCitations } from '../../utils/preprocessCitations.js';
import { getChunk } from '../../services/api.js';


const ChatContainer = ({messages,setSourceBar,setSourceBarSources
     ,documentSourceCache,setDocumentSourceCache,showContent,documentContent
}) => {
  
 async function openCitation(ids,citations){
  
    const idSet = new Set(ids);
    const sideSources =[];
    const selectedSources = citations.filter(source =>
      idSet.has(source.citationNumber)
    );

    for(const source of selectedSources){
       const cache = documentSourceCache[source.chunkId];
      if(cache){
        sideSources.push(cache);
      }else{
      const chunk = await getChunk(source.chunkId);
      chunk.citationNumber = source.citationNumber;

      sideSources.push(chunk);

      setDocumentSourceCache(prev => ({
          ...prev, 
          [source.chunkId]: chunk,
      }));
      }
    }
    console.log('sideSources - ',sideSources);

    setSourceBarSources(sideSources)
    setSourceBar(true);
  }

  return (
    <div className="chat-container">
  {
  showContent?
  ( <div className="message assistant">
    <div className="message-content markdown">
    
    
     
    <ReactMarkdown remarkPlugins={[remarkGfm]}>
      {documentContent}
    </ReactMarkdown>
    
    </div>
  </div>):   
  (messages.map((message, index) => (
    <div
      key={index}
      className={`message ${message.role}`}
    >
      {message.role === "assistant" && (
        <img
          src={assets.ai_icon}
          alt=""
          className="avatar"
        />
      )}

     <div className="message-content">

  {
  message.loading
    ? message.status
    : (
  
   
<ReactMarkdown
    rehypePlugins={[rehypeRaw]}
  components={{
    citation({ node }) {

        const ids = node.properties.ids
            .split(",")
            .map(id => Number(id.trim()));

        return (
            <Citation
                ids={ids}
                onClick={() => openCitation(ids,message.citations)}
            />
        );
    }
}}
>
    {preprocessCitations(message.content)}
</ReactMarkdown>

       
      )
}
</div>
    </div>
  )))}
</div>
  )
}

export default ChatContainer