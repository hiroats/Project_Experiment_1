import React, { useState } from 'react';

function Signup() {
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [error, setError] = useState(null);

    const handleUsernameChange = (e) => setUsername(e.target.value);
    const handlePasswordChange = (e) => setPassword(e.target.value);

    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            const response = await fetch('/signup', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ username, password }),
            });
            if (response.ok) {
                window.location.href = '/login'; // サインアップ成功時にリダイレクト
            } else {
                setError('サインアップに失敗しました。');
            }
        } catch (err) {
            setError('エラーが発生しました。もう一度お試しください。');
        }
    };

    return (
        <div>
            <h1>サインアップ</h1>
            <form onSubmit={handleSubmit}>
                <label htmlFor="username">ユーザー名:</label>
                <input
                    type="text"
                    id="username"
                    value={username}
                    onChange={handleUsernameChange}
                    required
                />
                
                <label htmlFor="password">パスワード:</label>
                <input
                    type="password"
                    id="password"
                    value={password}
                    onChange={handlePasswordChange}
                    required
                />
                
                <button type="submit">サインアップ</button>
            </form>
            {error && <p>{error}</p>}
            <p><a href="/login">ログインはこちら</a></p>
        </div>
    );
}

export default Signup;
