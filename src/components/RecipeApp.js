import React from 'react';
import { Link } from 'react-router-dom';

function RecipeApp() {
    const handlePredictCategory = async () => {
        const ingredients = document.getElementById('ingredients').value;

        try {
            const response = await fetch('/predict_category', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ ingredients }),
            });
            const data = await response.json();

            let output = '<h2>おすすめのカテゴリ</h2><ul>';
            if (data.error) {
                output += `<li>エラー: ${data.error}</li>`;
            } else {
                for (const [category, prob] of Object.entries(data)) {
                    output += `<li>${category}: ${prob.toFixed(2)}%</li>`;
                }
            }
            output += '</ul>';
            document.getElementById('category_prediction').innerHTML = output;
        } catch (error) {
            console.error('エラー:', error);
        }
    };

    return (
        <div className="container">
            <h1>レシピ提案アプリ</h1>
            <form id="recipeForm" action="/get_recipe" method="post">
                <label htmlFor="ingredients">食材を入力してください:</label>
                <input type="text" id="ingredients" name="ingredients" required />

                <button type="button" onClick={handlePredictCategory}>おすすめカテゴリを予測</button>
                <div id="category_prediction"></div>

                <label htmlFor="category">料理の種類を選択してください:</label>
                <select id="category" name="category" required>
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

            <div id="recipe-result"></div>

            <nav>
                <Link to="/upload">レシピ追加</Link>
                <Link to="/logout">ログアウト</Link>
            </nav>
        </div>
    );
}

export default RecipeApp;
