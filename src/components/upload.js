import React, { useState } from 'react';

function UploadRecipe() {
    const [title, setTitle] = useState('');
    const [category, setCategory] = useState('');
    const [ingredients, setIngredients] = useState('');
    const [recipeUrl, setRecipeUrl] = useState('');
    const [error, setError] = useState(null);
    const [success, setSuccess] = useState(null);

    const handleTitleChange = (e) => setTitle(e.target.value);
    const handleCategoryChange = (e) => setCategory(e.target.value);
    const handleIngredientsChange = (e) => setIngredients(e.target.value);
    const handleRecipeUrlChange = (e) => setRecipeUrl(e.target.value);

    const handleSubmit = async (e) => {
        e.preventDefault();
        const formData = new FormData();
        formData.append('title', title);
        formData.append('category', category);
        formData.append('ingredients', ingredients);
        formData.append('recipe_url', recipeUrl);

        try {
            const response = await fetch('/upload-recipe', {
                method: 'POST',
                body: formData,
            });
            if (response.ok) {
                setSuccess('レシピがアップロードされました。');
                setError(null);
            } else {
                setError('レシピのアップロードに失敗しました。');
            }
        } catch (err) {
            setError('エラーが発生しました。もう一度お試しください。');
            setSuccess(null);
        }
    };

    return (
        <div>
            <h1>新しいレシピ</h1>
            <form onSubmit={handleSubmit}>
                <label htmlFor="title">レシピ名:</label>
                <input
                    type="text"
                    name="title"
                    value={title}
                    onChange={handleTitleChange}
                    required
                /><br />

                <label htmlFor="category">カテゴリー:</label>
                <input
                    type="text"
                    name="category"
                    value={category}
                    onChange={handleCategoryChange}
                    required
                /><br />

                <label htmlFor="ingredients">材料:</label>
                <input
                    type="text"
                    name="ingredients"
                    value={ingredients}
                    onChange={handleIngredientsChange}
                    required
                /><br />

                <label htmlFor="recipe_url">レシピURL:</label>
                <input
                    type="text"
                    name="recipe_url"
                    value={recipeUrl}
                    onChange={handleRecipeUrlChange}
                /><br />

                <button type="submit">Upload Recipe</button>
            </form>
            {error && <p>{error}</p>}
            {success && <p>{success}</p>}
        </div>
    );
}

export default UploadRecipe;
