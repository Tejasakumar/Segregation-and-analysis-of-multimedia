import React from 'react'
import Navigation from '../components/Navigation'
import MLGeneralFolderList from '../components/MLFolderList'
import NudeFolderList from '../components/NudeFolderList'
import FaceFolderListOuter from '../components/FaceFolderListOuter'
import { Link } from 'react-router-dom'
function MlDirs() {
  return (
    <div>
      <Navigation>
        <Link to="face">
        View all the faces
        </Link>
      </Navigation>
      <MLGeneralFolderList/>
      <NudeFolderList/>
      {/* <FaceFolderListOuter/> */}
    </div>
  )
}

export default MlDirs
