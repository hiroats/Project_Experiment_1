import React, { useState, useEffect } from 'react';
import ReactDom from 'react-dom';
import App from './App';

ReactDom.render(<App />, document.getElementById('root'));

function RecipeApp() {
    const [ingredients, setIngredients] = useState('');
    const [category, setCategory] = useState('all');
    const [recipes, setRecipes] = useState([]);
    const [error, setError] = useState(null);

    const handleIngredientsChange = (e) => setIngredients(e.target.value);
    const handleCategoryChange = (e) => setCategory(e.target.value);

    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            const response = await fetch('/get_recipe', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ ingredients, category }),
            });
            const data = await response.json();
            setRecipes(data.recipes);
            setError(null);
        } catch (err) {
            setError('レシピの取得に失敗しました。');
        }
    };

    return (
        <div className="container">
            <h1>レシピ提案アプリ</h1>
            <form onSubmit={handleSubmit}>
                <label htmlFor="ingredients">食材を入力してください:</label>
                <input
                    type="text"
                    id="ingredients"
                    value={ingredients}
                    onChange={handleIngredientsChange}
                    required
                />

                <label htmlFor="category">料理の種類を選択してください:</label>
                <select id="category" value={category} onChange={handleCategoryChange} required>
                    <option value="all">全て</option>
                    <option value="japanese">和食</option>
                    <option value="italian">イタリアン</option>
                    <option value="chinese">中華</option>
                    <option value="korean">韓国料理</option>
                    <option value="ethnic">エスニック</option>
                    <option value="french">フレンチ</option>
                </select>

                <button type="submit">レシピを提案</button>
            </form>

            <div id="recipe-result">
                {recipes.length > 0 ? (
                    <>
                        <h2>検索結果:</h2>
                        <ul>
                            {recipes.map((recipe, index) => (
                                <li key={index}>
                                    <h3>{recipe.title}</h3>
                                    <p>カテゴリー: {recipe.category}</p>
                                    <p>材料: {recipe.ingredients}</p>
                                    <a href={recipe.recipe_url}>レシピを見る</a>
                                    {recipe.image_url && <img src={recipe.image_url} alt={recipe.title} />}
                                </li>
                            ))}
                        </ul>
                    </>
                ) : (
                    <p>レシピが見つかりませんでした。</p>
                )}
                {error && <p>{error}</p>}
            </div>

            <div>
                <a href="/logout">ログアウト</a>
                <a href="/upload">レシピ追加</a>
            </div>
        </div>
    );
}

export default RecipeApp;
