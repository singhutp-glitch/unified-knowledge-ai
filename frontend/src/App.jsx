
import { useState ,useEffect} from "react"
import ChatPage from "./components/ChatPage/ChatPage";
import Register from './components/RegisterPage/RegisterPage'
import LoginPage from "./components/LoginPage/LoginPage";
import { getUser } from "./services/authApi";
import StartupScreen from './components/StartupScreen/StartupScreen'
import { waitForBackend } from "./services/backendInitialize.js";
const ENABLE_STARTUP_SCREEN = import.meta.env.ENABLE_STARTUP_SCREEN === 'true';

function App() {
  const [user, setUser] = useState(null);
  const [authMode, setAuthMode] = useState("login");
  const [backendReady, setBackendReady] = useState(false);

    useEffect(() => {
        
        async function initialize() {
            if(ENABLE_STARTUP_SCREEN){
              await waitForBackend();
            }
          
            await getUserInfo();
            setBackendReady(true);
        }

        initialize();
    }, []);

    async function getUserInfo() {

    if (!localStorage.getItem("token")) {
      return;
    }

    try {
      const user = await getUser();

      setUser(user);
    } catch (error) {
      localStorage.removeItem("token");
    }}; 


function onLogout(){
  localStorage.removeItem('token');
  setUser(null)
}

    if (!backendReady) {
        return <StartupScreen />;
    }

  return (
    <>

      {user?<ChatPage onLogout={onLogout}  user={user}/>:
      authMode==='register'?<Register setAuthMode={setAuthMode} />:
      <LoginPage setUser={setUser} setAuthMode={setAuthMode}/>}    
    </>
  )
}

export default App
