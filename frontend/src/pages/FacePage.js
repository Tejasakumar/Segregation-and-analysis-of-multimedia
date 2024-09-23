import React, { useEffect,useState } from 'react'
import FaceDragDrop from '../components/FaceDragnDrop'
import Navigation from '../components/Navigation'
import FaceFolderList from '../components/FaceFolderList'
import { Link } from 'react-router-dom'
import axios from 'axios'

function FacePage() {
    const [loading, setLoading] = useState(true)
    useEffect(()=>{
        axios.get("http://127.0.0.1:5000/faces").then((res)=>{
            console.log(res);
            setLoading(false)
        })
        .catch((err)=>{
            console.log(err);
        })
    })
    if (loading) {
        return(
            <div>
                loading.....
            </div>
        )
    }
    return (
        <div >
            <Navigation style={{ marginRight: "35%" }} />
            <FaceDragDrop />
            <Link to=".." className="back-button" relative="path">
				← Back to Folders
			</Link>
            <div style={{ marginRight: "35%" }}>
                <FaceFolderList />
            </div>
        </div>
    )
}

export default FacePage