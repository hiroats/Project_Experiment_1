import React from 'react';
import { Routes, Route } from 'react-router-dom';
import RecipeApp from './RecipeApp';
import Login from './Login';
import Signup from './Signup';
import Upload from './Upload';

function App() {
    return (
        <Routes>
            <Route path="/" element={<RecipeApp />} />
            <Route path="/login" element={<Login />} />
            <Route path="/signup" element={<Signup />} />
            <Route path="/upload" element={<Upload />} />
        </Routes>
    );
}

export default App;
