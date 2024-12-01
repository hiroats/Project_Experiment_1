import React from "react";
import { BrowserRouter as Router, Routes, Route, Link } from "react-router-dom";
import Login from "./Login";
import Signup from "./Signup";
import Upload from "./Upload";

const RecipeApp = () => {
    return (
        <Router>
            <div className = "container">
                <header>
                    <h1>レシピ提案アプリ</h1>
                    <nav>
                        <ul>
                            <li><Link to="/">ホーム</Link></li>
                            <li><Link to="/login">ログイン</Link></li>
                            <li><Link to="/signup">サインアップ</Link></li>
                            <li><Link to="/upload">レシピ追加</Link></li>
                        </ul>
                    </nav>
                </header>

                <main>
                    <Routes>
                        <Route path="/" element={<Home />} />
                        <Route path="/login" element={<Login />} />
                        <Route path="/signup" element={<Signup />} />
                        <Route path="/upload" element={<Upload />} />
                    </Routes>
                </main>
            </div>
        </Router>
    );
};

const Home = () => (
    <div>
        <h2>ようこそ！</h2>
        <p>こちらはレシピ提案アプリです。メニューから選択してください。</p>
    </div>
);

export default RecipeApp;