<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Movie Catalog</title>
    <link href="output.css" rel="stylesheet">
</head>
<body class="bg-neutral-900 text-neutral-200">

<div class="container mx-auto max-w-screen-lg">
    <h1 class="text-4xl font-bold text-center text-neutral-100 mb-6 mt-8">Movie Catalog</h1>

    <!-- Форма для пошуку, фільтрації та сортування -->
    <div class="flex justify-center mb-8">
        <form id="search-form" class="w-full max-w-2xl flex flex-wrap gap-4">
            <!-- Поле для пошуку за назвою -->
            <input type="text" name="title" placeholder="Search by title" class="flex-grow p-2 rounded bg-neutral-800 text-neutral-200" />

            <!-- Фільтр за жанром -->
            <select name="genre" class="flex-1 p-2 rounded bg-neutral-800 text-neutral-200">
                <option value="">All Genres</option>
                <option value="Action">Action</option>
                <option value="Comedy">Comedy</option>
                <option value="Drama">Drama</option>
            </select>

            <!-- Фільтр за роком -->
            <select name="year" class="flex-1 p-2 rounded bg-neutral-800 text-neutral-200">
                <option value="">All Years</option>
                <?php for ($year = date("Y"); $year >= 1900; $year--): ?>
                    <option value="<?php echo $year; ?>"><?php echo $year; ?></option>
                <?php endfor; ?>
            </select>

            <!-- Фільтр за рейтингом -->
            <select name="rating" class="flex-1 p-2 rounded bg-neutral-800 text-neutral-200">
                <option value="">All Ratings</option>
                <option value="9">9+</option>
                <option value="8">8+</option>
                <option value="7">7+</option>
            </select>

            <!-- Сортування фільмів -->
            <select id="sort" name="sort" class="flex-1 p-2 rounded bg-neutral-800 text-neutral-200">
                <option value="title-asc">Sort by Title (A-Z)</option>
                <option value="title-desc">Sort by Title (Z-A)</option>
                <option value="year-asc">Sort by Year (Oldest First)</option>
                <option value="year-desc">Sort by Year (Newest First)</option>
                <option value="rating-desc">Sort by Rating (High to Low)</option>
                <option value="rating-asc">Sort by Rating (Low to High)</option>
            </select>

            <!-- Кнопка пошуку -->
            <button type="submit" class="p-2 rounded bg-red-500 text-neutral-100 hover:bg-red-600">Search</button>
        </form>
    </div>

    <!-- Контейнер для відображення карток фільмів -->
    <div id="movie-container" class="flex flex-wrap gap-6 justify-center"></div>
    <div id="loading" style="text-align: center; display: none;">Loading...</div>
</div>

<!-- Кнопка "Повернутися нагору" -->
<button id="back-to-top" class="fixed bottom-4 right-4 hidden p-3 bg-red-500 text-white rounded-full">
    ↑
</button>

<script src="script.js"></script>
</body>
</html>
