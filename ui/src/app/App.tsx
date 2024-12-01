import React from 'react';
import logo from './logo.svg';
import './App.css';
import Chat from "../view/view.chat";
import {Box} from "@mui/material";
import camo from "./camo.jpg";

function App() {
    return (
        <Box sx={{
            backgroundImage: `url(${camo})`,
            height: "100vh",
            backgroundColor: "rgba(0, 0, 0, .1)",
            backgroundBlendMode: "multiply"
        }}>
            <Box sx={{display: "flex", justifyContent: "center", paddingTop: 4}}>
                <Chat/>
            </Box>
        </Box>

    );
}

export default App;
