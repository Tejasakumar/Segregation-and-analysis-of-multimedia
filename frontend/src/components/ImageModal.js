import React from "react";
import "./Imagemodal.css"; // Make sure to create this CSS file

function Imagemodal({ image, onClose }) {
	console.log("Modal image:", image); // Add this line for debugging

	if (!image) return null;
	const handleDownload = () => {
		// Create a temporary link element
		const link = document.createElement("a");
		link.href = image;
		const fileExtension = "png"; // Get the extension from the URL
		link.download = `downloaded_image.${fileExtension}`; // Specify the desired file name with extension
		document.body.appendChild(link);
		link.click();
		document.body.removeChild(link);
	  };
	return (
		<div className="image-modal">
			<div className="image-modal-content">
				<img src={image} alt="Full size" style={{height:100+"%"}} />
			</div>
			<button className="close" onClick={onClose}>Close</button>
			<button className="censor" onClick={handleDownload}>Download</button>		
		</div>
	);
}

export default Imagemodal;
