import React, { useState, useEffect, useContext } from 'react';
import { Link } from 'react-router-dom';
import axios from 'axios';
import './Folder.css';
import { unclassified_images } from "../pages/Landing";
import { io } from "socket.io-client";

function FaceFolderList() {
	const [folders, setFolders] = useState({});
	const [loading, setLoading] = useState(true);
	const [sockdata, setscokdata] = useContext(unclassified_images)
	const [socket, setSocket] = useState(null)

	console.log("folders", folders);
	// useEffect(() => {
	// 	setFolders(sockdata)
	// 	setLoading(false)
	// }, [sockdata])


	useEffect(() => {
		if (!socket) {
			const sockk = io("http://127.0.0.1:5000/face");
			setSocket(sockk)
			sockk.emit("Ready");
		}
		if (socket) {
			socket.on("image_name", (data) => {
				if(loading){
					setLoading(false)
				}
				console.log("image _name ",data.content);
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

	if (loading) {
		return <div>Loading...</div>;
	}

	return (
		<div className="folder-list">
			{Object.keys(folders).map((folder, index) => (
				<Link
					to={`folder/${index}`}
					key={index}
					className="folder-item"
					state={{
						data: folders[folder][0].data,
						collection: folder,
						identity: folders[folder][0].id,
						db:"faces"
					}}
				>
					<div className="folder-thumbnail">
						{
							// <img src={`data:image/jpeg;base64,${folders[folder]}`} alt={folder} />
							<img src={folders[folder][0].data} />
						}
					</div>
					<div className="folder-name">{folder}</div>
					{/* <div className="file-count">{folder.Number_of_files} files</div> */}
				</Link>
			))}
		</div>
	);
}

export default FaceFolderList;