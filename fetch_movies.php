<?php
// Підключення конфігураційного файлу
$config = include 'config.php';

// Отримання налаштувань бази даних з конфігурації
$host = $config['host'];
$db = $config['db'];
$user = $config['user'];
$pass = $config['pass'];

// Параметри підключення до бази даних
$dsn = "mysql:host=$host;dbname=$db;charset=utf8mb4";
$options = [
    PDO::ATTR_ERRMODE            => PDO::ERRMODE_EXCEPTION,
    PDO::ATTR_DEFAULT_FETCH_MODE => PDO::FETCH_ASSOC,
];

try {
    // Встановлення з'єднання з базою даних
    $pdo = new PDO($dsn, $user, $pass, $options);
} catch (PDOException $e) {
    // Обробка помилки підключення
    http_response_code(500);
    echo $e->getMessage();
    exit;
}

// Отримуємо поточну сторінку та параметри запиту
$page = isset($_GET['page']) ? (int)$_GET['page'] : 1;
$title = isset($_GET['title']) ? $_GET['title'] : '';
$genre = isset($_GET['genre']) ? $_GET['genre'] : '';
$year = isset($_GET['year']) ? (int)$_GET['year'] : '';
$rating = isset($_GET['rating']) ? (int)$_GET['rating'] : '';
$sort = isset($_GET['sort']) ? $_GET['sort'] : 'title-asc';

$limit = 10;
$offset = ($page - 1) * $limit;

// Створюємо SQL-запит з урахуванням фільтрів
$query = "SELECT title, poster_url, year, plot, imdb_id AS imdbID FROM movies WHERE 1=1";
$params = [];

// Додаємо умови фільтрації до запиту
if ($title) {
    $query .= " AND title LIKE :title";
    $params['title'] = "%$title%";
}

if ($genre) {
    $query .= " AND genre LIKE :genre";
    $params['genre'] = "%$genre%";
}

if ($year) {
    $query .= " AND year = :year";
    $params['year'] = $year;
}

if ($rating) {
    $query .= " AND imdb_rating >= :rating";
    $params['rating'] = $rating;
}

// Додаємо сортування
$orderBy = 'title ASC';
switch ($sort) {
    case 'title-desc':
        $orderBy = 'title DESC';
        break;
    case 'year-asc':
        $orderBy = 'year ASC';
        break;
    case 'year-desc':
        $orderBy = 'year DESC';
        break;
    case 'rating-asc':
        $orderBy = 'imdb_rating ASC';
        break;
    case 'rating-desc':
        $orderBy = 'imdb_rating DESC';
        break;
}

$query .= " ORDER BY $orderBy LIMIT :limit OFFSET :offset";

$stmt = $pdo->prepare($query);

// Прив'язуємо параметри до запиту
foreach ($params as $key => $value) {
    $stmt->bindValue(":$key", $value, is_int($value) ? PDO::PARAM_INT : PDO::PARAM_STR);
}
$stmt->bindValue(':limit', $limit, PDO::PARAM_INT);
$stmt->bindValue(':offset', $offset, PDO::PARAM_INT);
$stmt->execute();

// Отримуємо результати запиту
$movies = $stmt->fetchAll();

// Повертаємо результати у форматі JSON
header('Content-Type: application/json');
echo json_encode($movies);
