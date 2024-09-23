import {React,useState} from "react";
import "./Imagemodal.css"; 

function Nude_modal({ image, onClose }) {
	console.log("Modal image:", image); // Add this line for debugging
	const [Image, setImage] = useState(image[0])
	const [index, setindex] = useState(0)

	if (!image) return null;
	const togle =()=>{
		setImage(image[(index+1)%2])
		setindex((index+1)%2)
	}
	return (
		<div className="image-modal">
			<div className="image-modal-content">
				<img src={Image} alt="Full size" style={{height:100+"%"}} />
				<button className="close" onClick={onClose}>Close</button>
				<button className="censor" onClick={togle}>show {index === 0 ? 'unsensored' : 'censored'}</button>		
			</div>
			
		</div>
	);
}

export default Nude_modal;
