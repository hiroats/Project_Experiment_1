import React from 'react';
import { Link } from 'react-router-dom';

function Signup() {
    return (
        <div>
            <h1>サインアップ</h1>
            <form action="/signup" method="post">
                <label htmlFor="username">ユーザー名:</label>
                <input type="text" id="username" name="username" required />

                <label htmlFor="password">パスワード:</label>
                <input type="password" id="password" name="password" required />

                <button type="submit">サインアップ</button>
            </form>
            <p>
                <Link to="/login">ログインはこちら</Link>
            </p>
        </div>
    );
}

export default Signup;
