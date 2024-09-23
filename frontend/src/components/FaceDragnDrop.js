import React, { useState } from "react";
import { FileUploader } from "react-drag-drop-files";
import "./FaceDragDrop.css";
import axios from "axios";

const fileTypes = ["JPG", "PNG", "GIF", "JPEG"];

function FaceDragDrop() {
	const [file, setFile] = useState(null);
	const handleChange = (file) => {
		setFile(file);
	};
	const [resdata, setresdata] = useState(null)
	const sendImageToRecognition = () => {
		if (file) {
			const reader = new FileReader();
			reader.onload = (event) => {
				const fileContents = event.target.result.split(",")[1];
                // console.log("File contents:", fileContents);
                axios.post("http://127.0.0.1:5000/test", {fileContents})
                    .then((res) => {
                        console.log(res);
						setresdata(res.data)
                        setFile(null)
                    })
                    .catch((err) => {
                        console.log(err);
                    });
				
			};
			reader.readAsDataURL(file);
		}
	};

	return (
		<div className="side-panel">
			<h2>Upload Image</h2>
			<FileUploader handleChange={handleChange} types={fileTypes}>
				<div
					style={{
						border: "2px dashed #0f0f0f",
						borderRadius: "10px",
						height: "300px",
						width: "90%",
						margin: "auto",
						display: "flex",
						flexDirection: "column",
						justifyContent: "center",
						alignItems: "center",
						verticalAlign: "center",
						padding: "20px",
						boxSizing: "border-box",
						backgroundColor: "rgba(0, 0, 0, 0.2)",
					}}
				>
					<p style={{ textAlign: "center", fontSize: "18px" }}>
						Drag and drop a face here to get all the similar Faces
					</p>
					<p style={{ textAlign: "center", fontSize: "20px" }}> or </p>
					<p style={{ textAlign: "center", fontSize: "18px" }}>
						Click here to browse from your local file system
					</p>
				</div>
			</FileUploader>
			<button
				onClick={sendImageToRecognition}
				disabled={file === null}
				className="submit-button"
			>
				Get Similar Faces
			</button>
			{resdata && <div> please check {resdata} </div>}
		</div>
	);
}

export default FaceDragDrop;
