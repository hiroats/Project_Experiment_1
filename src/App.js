// App.js
import React from 'react';
import { BrowserRouter as Router, Route, Switch, Link } from 'react-router-dom';
import Login from './login';
import Signup from './signup';
import UploadRecipe from './upload';
import RecipeApp from './RecipeApp';

function App() {
    return (
        <Router>
            <div>
                <nav>
                    <Link to="/">ホーム</Link> | <Link to="/login">ログイン</Link> | <Link to="/signup">サインアップ</Link> | <Link to="/upload">レシピ追加</Link>
                </nav>
                <Switch>
                    <Route exact path="/" component={RecipeApp} />
                    <Route path="/login" component={Login} />
                    <Route path="/signup" component={Signup} />
                    <Route path="/upload" component={UploadRecipe} />
                </Switch>
            </div>
        </Router>
    );
}

export default App;
