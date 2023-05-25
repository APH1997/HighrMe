import { createContext, useContext, useState} from "react";

export const TabContext = createContext()

export function TabContextProvider(props){
    const [tab, setTab] = useState('photos')
    return (
        <TabContext.Provider value={{tab, setTab}}>
            {props.children}
        </TabContext.Provider>
    )
}

export const useTab = () => useContext(TabContext)
