import React, { useState } from 'react';

function Login() {
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [error, setError] = useState(null);

    const handleUsernameChange = (e) => setUsername(e.target.value);
    const handlePasswordChange = (e) => setPassword(e.target.value);

    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            const response = await fetch('/login', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ username, password }),
            });
            if (response.ok) {
                window.location.href = '/'; // ログイン成功時にリダイレクト
            } else {
                setError('ログインに失敗しました。ユーザー名またはパスワードを確認してください。');
            }
        } catch (err) {
            setError('エラーが発生しました。もう一度お試しください。');
        }
    };

    return (
        <div>
            <h1>ログイン</h1>
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
                
                <button type="submit">ログイン</button>
            </form>
            {error && <p>{error}</p>}
            <p><a href="/signup">サインアップはこちら</a></p>
        </div>
    );
}

export default Login;
