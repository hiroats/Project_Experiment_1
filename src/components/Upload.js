import React from 'react';

function Upload() {
    return (
        <div>
            <h1>新しいレシピを追加</h1>
            <form action="/upload-recipe" method="post" encType="multipart/form-data">
                <label htmlFor="title">レシピ名:</label>
                <input type="text" id="title" name="title" required />

                <label htmlFor="category">カテゴリー:</label>
                <input type="text" id="category" name="category" required />

                <label htmlFor="ingredients">材料:</label>
                <input type="text" id="ingredients" name="ingredients" required />

                <label htmlFor="recipe_url">レシピURL:</label>
                <input type="text" id="recipe_url" name="recipe_url" />

                <button type="submit">Upload Recipe</button>
            </form>
        </div>
    );
}

export default Upload;
