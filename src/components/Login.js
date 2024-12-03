import React from 'react';
import { Link } from 'react-router-dom';

function Login() {
    return (
        <div>
            <h1>ログイン</h1>
            <form action="/login" method="post">
                <label htmlFor="username">ユーザー名:</label>
                <input type="text" id="username" name="username" required />

                <label htmlFor="password">パスワード:</label>
                <input type="password" id="password" name="password" required />

                <button type="submit">ログイン</button>
            </form>
            <p>
                <Link to="/signup">サインアップはこちら</Link>
            </p>
        </div>
    );
}

export default Login;
