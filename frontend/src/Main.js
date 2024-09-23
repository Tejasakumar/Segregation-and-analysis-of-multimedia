import React from "react";
import "./Main.css";
import "./fonts/Raleway-VariableFont_wght.ttf";
import { Link } from "react-router-dom";

const MainComponent = () => {
	return (
		<div
			style={{
				fontFamily: "Medium",
				textAlign: "center",
				alignItems: "center",
			}}
		>
			<h1>Main Page</h1>
			<Link to="location" target="blank">
				<button
					style={{
						fontFamily: "Medium",
						top: "30%",
						left: "35%",
						position: "absolute",
					}}
				>
					<span>Open App 1 (Location) </span>
				</button>
			</Link>
			<Link to="timeline" target="blank">
				<button
					style={{
						fontFamily: "Medium",
						top: "40%",
						left: "35%",
						position: "absolute",
					}}
				>
					<span>Open App 2 (Timeline) </span>
				</button>
			</Link>
			<Link to="noEXIF" target="blank" >
				<button
					style={{
						fontFamily: "Medium",
						top: "50%",
						left: "35%",
						position: "absolute",
					}}
				>
					<span>Open App 3 (No EXIF) </span>
				</button>
			</Link>
		</div>
	);
};

export default MainComponent;
