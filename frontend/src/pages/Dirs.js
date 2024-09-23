import { React, useState, useContext, useEffect } from "react";
import Navbar from "../components/Navigation";
import Button from "../components/Button";
import Checklist from "../components/Checkslit";
import FolderList from "../components/FolderList";
import Sidepanel from "../components/Sidepanel";
import { Link, useLocation } from "react-router-dom";
import { unclassified_images } from "../pages/Landing";
import io from "socket.io-client";
import axios from "axios";

function Dirs() {
	const [data, setData] = useContext(unclassified_images);
	const [hidden, setHidden] = useState(true);
	const [blur, setBlur] = useState(false);
	const [display, setDisplay] = useState({});
	// console.log(display);
	const check_list = () => {
		setHidden(false);
		setBlur(true);
	};
	const call_by_check_to_reset = () => {
		setHidden(true);
		setBlur(false);
	};
	useEffect(() => {
		setDisplay(data)
	},[data])
	return (
		<div>
			<dir style={blur ? { filter: "blur(8px)" } : {}}>
				<Navbar />
				<FolderList />
				<div style={{padding:"3%", textAlign:"center", justifySelf:"center" }}>
					<Button val="Analyze Using AI" onClick={check_list} />
					<Link to="/ta">
						<Button val="Timeline Analysis" />
					</Link>
				</div>
			</dir>
			{!hidden && <Checklist reset={call_by_check_to_reset} />}
			{/* <Sidepanel>magu</Sidepanel> */}
			{/* <button onClick={handleSocketEvent}>Click me </button> */}
			<div>
				{/* {display.map((data, index) => (
					<img src={data} alt="image" style={{ width: 10 + "%" }} />
				))} */}
			</div>
		</div>
	);
}

export default Dirs;
