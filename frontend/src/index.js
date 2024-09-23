import React from "react";
import ReactDOM from "react-dom/client";
import "./index.css";
import DumpUpload from "./pages/DumpUpload";
import PhotoUpload from "./pages/PhotoUpload";
import Dirs from "./pages/Dirs";
import FolderView from "./components/FolderView";
import Landing, { ModelLoad, UnclassifiedImagesProvider } from "./pages/Landing";
import reportWebVitals from "./reportWebVitals";
import "bootstrap/dist/css/bootstrap.css";
import { createBrowserRouter, RouterProvider } from "react-router-dom";
import Loading from "./pages/Loading";
import MlDirs from "./pages/MlDirs";
import NudeFolderView from "./components/NudeFolderView";
import FaceDragDrop from "./components/FaceDragnDrop";
import FacePage from "./pages/FacePage";
import FaceFolderView from "./components/FaceFolderView";
import MaingComponent from "./Main"
import Location from "./pages/location-page"
import NoEXIF from "./pages/no-exif-page"
import TimelinePage from "./pages/timeline-page";
import ChatPage from "./pages/ChatPage";

const router = createBrowserRouter([
	{ path: "/", element: <Landing /> },
	{ path: "/only-image", element: <PhotoUpload /> },
	{ path: "/forensic-image", element: <DumpUpload /> },
	
	{ path: "/loading", element: <Loading /> },
	{ path: "/directory",element: <Dirs />,},
	{ path: "/mldirectory", element: <MlDirs/> },
	
	{ path: "/directory/folder/:id", element: <FolderView /> },
	{ path: "/mldirectory/folder/:id", element: <FolderView /> },
	{ path: "/mldirectory/faces", element: <MlDirs /> },
	{ path: "/mldirectory/folder/nudes", element: <NudeFolderView /> },
	{ path: "/mldirectory/folder/nudes", element: <NudeFolderView /> },
	{ path: "/mldirectory/face", element: <FacePage /> },
	{ path: "/mldirectory/face/folder/:id", element: <FaceFolderView /> },
	{ path: "/test", element: <FaceDragDrop /> },
	{ path: "/chat", element: <ChatPage/> },
	
	{ path: "/ta", element: <MaingComponent/> },
	{ path: "/ta/location", element: <Location /> },
	{ path: "/ta/timeline", element: <TimelinePage /> },
	{ path: "/ta/noExif", element: <NoEXIF /> },


	
]);

const root = ReactDOM.createRoot(document.getElementById("root"));
root.render(
	<React.StrictMode>
		<ModelLoad>
		<UnclassifiedImagesProvider>
			<RouterProvider router={router} />
		</UnclassifiedImagesProvider>
		</ModelLoad>
	</React.StrictMode>
);
