import React, { useState, useEffect, useContext } from 'react';
import { Link } from 'react-router-dom';
import axios from 'axios';
import './Folder.css';
import { unclassified_images,model_load } from "../pages/Landing";
import { io } from "socket.io-client";
import './mlcss.css'
import Nude_modal from './NudeModal';

function FaceFolderListOuter() {
    const [folders, setFolders] = useState({});
    const [loading, setLoading] = useState(false);
    const [sockdata, setscokdata] = useContext(unclassified_images)
    const [model,Setmodel] = useContext(model_load)
    const [socket, setSocket] = useState(null)
    console.log("folders", folders);
    // useEffect(() => {
    //     setFolders(sockdata)
    //     setLoading(false)
    //     if(!model ){
    //         Setmodel(true)
    //     }
    // }, [sockdata])


    useEffect(() => {
        if (!socket) {
            const sockk = io("http://127.0.0.1:5000/Check");
            setSocket(sockk)
            sockk.emit("Ready");
        }
        if (socket) {
            socket.on("image_name", (data) => {
                console.log("image _name ", data.content);
                setFolders((prevData) => {
                    if (data.folder in prevData) {
                        return {
                            ...prevData,
                            [data.folder]: [...prevData[data.folder], data.content],
                        };
                    } else {
                        return {
                            ...prevData,
                            [data.folder]: [data.content],
                        };
                    }
                });
            })
        }

    }, [socket])
    console.log(loading);
    if (loading) {
        return (<div className='loader' style={{display:'flex',justifyContent:"center",alignItems:'center' ,marginTop: 20+"%", marginLeft:50+"%"}} ></div>)
    }

    else {
        return (
            <div className="folder-list">
                {Object.keys(folders).map((folder, index) => (
                    <Link
                        to={`face`}
                        key={index}
                        className="folder-item"
                        state={{
                            data: folders[folder][0].data,
                            collection: folder,
                            identity: folders[folder][0].id,
                            db:"Mlgen"
                        }}
                    >
                        <div className="folder-name">{folder}</div>
                        {/* <div className="file-count">{folder.Number_of_files} files</div> */}
                    </Link>
                ))}
            </div>
        );
    }
}

export default FaceFolderListOuter;