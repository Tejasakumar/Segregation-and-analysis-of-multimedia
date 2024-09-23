import { React, useState, } from 'react'
import { FileUploader } from "react-drag-drop-files";
import Navigation from '../components/Navigation';
import axios from 'axios';

function ChatPage() {
	const [text, setText] = useState("");
	const [file, setFile] = useState(null);
	const [data, setData] = useState(null)
	const handleChange = (event) => {
		setText(event.target.value);

	};

	const handleFileUpload = (file) => {

		const reader = new FileReader();
		reader.onload = (event) => {
			const fileContents = event.target.result.split(",")[1];
			console.log(fileContents);
			setFile(fileContents)
			// console.log("File contents:", fileContents);
			// axios
			// 	.post("http://127.0.0.1:5000/test", { fileContents })
			// 	.then((res) => {
			// 		console.log(res);
			// 		setFile(null);
			// 	})
			// 	.catch((err) => {
			// 		console.log(err);
			// 	});
		};
		reader.readAsDataURL(file);
	};
	const handleSubmit = () => {
		axios
			.post("http://127.0.0.1:5000/file-summary", { file: file, prompt: text })
			.then((res) => {
				console.log(res.data);
				setData(res.data)
				// setFile(null);
				setText("");
			})
			.catch((err) => {
				console.log(err);
			});
	}
	return (
		<div>
			<Navigation />
			{file && data && <div style={{marginInline:"10%", marginTop:"2%", overflowY:"scroll", height:"400px"}}>
				<img src={"data:image;base64,"+file} alt="image " style={{height:"300px",display:'flex',flexDirection:"column"}}/>
				{data}
				</div>}
			<div
				style={{
					position: "absolute",
					top: "80%",
					left: "10%",
					alignItems: "center",
					backgroundColor: "#C9DABF",
					padding: "20px",
					borderRadius: "10px",
					width: "80%",
					maxHeight: "400px",
				}}
			>
				<div style={{ display: "flex", flexDirection: "column" }}>
					{!file && (
						<FileUploader handleChange={handleFileUpload}>
							<h6 style={{ cursor: "pointer" }}>
								&#x1F4CE;Click here to Upload file
							</h6>
						</FileUploader>
					)}
					{file && (
						<div style={{ display: "flex" }}>
							<>Uploaded file: {file.name} </>
							<div style={{ cursor: "pointer" }} onClick={() => setFile(null)}>&#10060;</div>
						</div>
					)}
					<div style={{ display: "flex", width: "100%" }}>
						<textarea
							placeholder="Input your prompt and image"
							value={text}
							onChange={handleChange}
							style={{
								width: "100%",
								margin: "5px",
								padding: "10px",
								borderRadius: "10px",
								border: "1px solid #ccc",
								color: "black",
								height: "50px",
								backgroundColor: "transparent",
								maxHeight: "200px", // Set max height for scroll
								overflowY: "auto", // Enable vertical scrolling
								resize: "none", // Disable resizing by user
							}}
						/>
						<button
							type="submit"
							disabled={!text}
							onClick={handleSubmit}
							style={{
								borderRadius: "10px",
								height: "50px",
								marginTop: "5px",
								backgroundColor: text ? "black" : "#ccc",
								color: "white",
								cursor: text ? "pointer" : "not-allowed",
							}}
						>
							<h2>↑</h2>
						</button>
					</div>
				</div>
			</div>
		</div>
	);
}

export default ChatPage