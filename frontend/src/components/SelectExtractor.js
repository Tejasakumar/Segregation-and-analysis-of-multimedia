import React, { useState } from "react";

const HorizontalRadioButtons = (Params) => {
	const [selectedOption, setSelectedOption] = useState("Scalpel");

	const handleOptionChange = (event) => {
		setSelectedOption(event.target.value);
		Params.onChange(event.target.value);
	};

	return (
		<div style={{ display: "flex", alignItems: "center", justifyContent: "center",fontSize:"20px" }}>
			<label style={{ marginRight: "20px" }}>
				<input
					type="radio"
					value="Scalpel"
					checked={selectedOption === "Scalpel"}
					onChange={handleOptionChange}
				/>
				Scalpel
			</label>
			<label style={{ marginRight: "20px" }}>
				<input
					type="radio"
					value="Foremost"
					checked={selectedOption === "Foremost"}
                    onChange={handleOptionChange}
				/>
				Foremost
			</label>
		</div>
	);
};

export default HorizontalRadioButtons;
