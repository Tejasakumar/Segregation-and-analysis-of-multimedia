import { React, useState, useEffect } from "react";
import { useParams, Link, useLocation } from "react-router-dom";
import "./Folder.css";
import axios from "axios";
import Nude_modal from "./NudeModal";

function NudeFolderView() {
    const location = useLocation();
    const [folder, setFolder] = useState([location.state.data]);
    const [ide, setide] = useState([location.state.identity]);
    const db = location.state.db
    const map = new Map()
    map.set(ide[0], folder[0])
    const [hashmap, sethash] = useState(new Map(map))
    const collection = location.state.collection;
    // const [page, setpage] = useState(1)
    const [quant, setquant] = useState(1);
    const [openedImage, setOpenedImage] = useState(null);

    const handleImageClick = (id, image) => {
		console.log("Image clicked:", id, image); // Add this line for debugging
		setOpenedImage({ id, image });
	};
    const pageSize = 18;
    console.log("map", hashmap);

    [...hashmap.entries()].map(([id, image], index) =>
                    
    {   console.log(id,image[1]);
    });
    const loadPhotos = (newPage) => {
        axios
            .get(
                `http://127.0.0.1:5000/fetchphotos?count=${newPage}&size=${pageSize}&coll=${collection}&db=${db}`
            )
            .then((res) => {
                console.log("res data", res.data.photos);
                if (res.data.photos) {
                    console.log(res.data.photos);
                    const newFolderItems = res.data.photos.map(
                        (photo) => {
                            const cval = `data:image;base64,${photo.censored_image}`
                            const uval = `data:image;base64,${photo.uncensored_image}`
                            return [cval,uval]
                        }
                    );
                    console.log("check array",newFolderItems);
                    // setquant(quant + res.data.photos.length);
                    // setFolder((prevFolder) => [...prevFolder, ...newFolderItems]);
                    res.data.photos.forEach((photo) => {
                        if (!hashmap.has(photo._id.$oid)) {
                            sethash((prevMap) => {
                                const newMap = new Map(prevMap);
                                const arr = [newFolderItems[0],newFolderItems[1]]
                                newMap.set(photo._id.$oid, newFolderItems[0]);
                                return newMap;
                            });
                        }
                    });


                }
            })
            .then((err) => {
                console.log(err);
            });
    };
    useEffect(() => {
        loadPhotos(hashmap.size); // Initial load of photos when component mounts
    }, []);
    useEffect(() => {
        const handleScroll = () => {
            if (
                window.innerHeight + document.documentElement.scrollTop >=
                document.documentElement.offsetHeight - 1
            ) {
                loadPhotos(hashmap.size);
            }
        };
        window.addEventListener("scroll", handleScroll);
        return () => window.removeEventListener("scroll", handleScroll);
    }, [hashmap.size]);

    // console.log(folder);

    return (
        <div className="folder-view">
            <Link to="../.." className="back-button" relative="path">
                ← Back to Folders
            </Link>
            <h2>{collection}</h2>
            <div className="image-grid">
                {[...hashmap.entries()].map(([id, image], index) => (
                    
                    <div key={id}
                    className="image-item"
                    onClick={() => handleImageClick(id, image)}>
                        <img src={image[0]}
                         alt={`Image ${index + 1}`} />
                    </div>
                ))}
            </div>
            {openedImage && (
				<Nude_modal
					image={openedImage.image}
					onClose={() => {
						console.log("Closing modal"); // Add this line for debugging
						setOpenedImage(null);
					}}
				/>
			)}
        </div>
    );  
}

export default NudeFolderView;
