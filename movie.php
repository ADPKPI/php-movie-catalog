<?php
// Include configuration file
$config = include 'config.php';

// Get database connection parameters
$host = $config['host'];
$db = $config['db'];
$user = $config['user'];
$pass = $config['pass'];

// Database connection settings
$dsn = "mysql:host=$host;dbname=$db;charset=utf8mb4";
$options = [
    PDO::ATTR_ERRMODE            => PDO::ERRMODE_EXCEPTION,
    PDO::ATTR_DEFAULT_FETCH_MODE => PDO::FETCH_ASSOC,
];

try {
    // Establish database connection
    $pdo = new PDO($dsn, $user, $pass, $options);
} catch (PDOException $e) {
    // Display database connection error
    http_response_code(500);
    echo "Database connection failed.";
    exit;
}

// Get imdbID from URL
$id = isset($_GET['id']) ? $_GET['id'] : null;
if (!$id) {
    echo "Invalid movie ID.";
    exit;
}

// Query database for movie details
$stmt = $pdo->prepare("SELECT * FROM movies WHERE imdb_id = :id");
$stmt->execute(['id' => $id]);
$movie = $stmt->fetch();

if (!$movie) {
    echo "Movie not found.";
    exit;
}

// Split genres for recommendations
$genres = explode(', ', $movie['genre']);

// Fetch random movies with the same genre
$genre = $genres[0]; // Use the first genre for simplicity
$stmt = $pdo->prepare("SELECT * FROM movies WHERE genre LIKE :genre AND imdb_id != :id ORDER BY RAND() LIMIT 8");
$stmt->execute(['genre' => "%$genre%", 'id' => $id]);
$similar_movies = $stmt->fetchAll();
?>

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title><?php echo htmlspecialchars($movie['title']); ?></title>
    <link href="output.css" rel="stylesheet">
</head>
<body class="bg-neutral-900 text-neutral-200">

<div class="container mx-auto p-6">
    <a href="index.php" class="text-neutral-400 hover:text-red-300">&larr; Back to Catalog</a>
    <div class="movie-details bg-neutral-800 p-8 rounded-lg shadow-lg mt-6">
        <img src="<?php echo htmlspecialchars($movie['poster_url']); ?>" alt="<?php echo htmlspecialchars($movie['title']); ?>" class="max-w-md mx-auto rounded-md mb-4">
        <h1 class="text-4xl font-bold text-neutral-100 mb-2"><?php echo htmlspecialchars($movie['title']); ?> (<?php echo htmlspecialchars($movie['year']); ?>)</h1>
        <p class="text-neutral-400 mb-4"><strong>Genre:</strong> <?php echo htmlspecialchars($movie['genre']); ?></p>
        <p class="text-neutral-400 mb-4"><strong>Director:</strong> <?php echo htmlspecialchars($movie['director']); ?></p>
        <p class="text-neutral-400 mb-4"><strong>Actors:</strong> <?php echo htmlspecialchars($movie['actors']); ?></p>
        <p class="text-neutral-300 mb-4"><?php echo htmlspecialchars($movie['plot']); ?></p>
        <p class="text-neutral-400"><strong>IMDB Rating:</strong> <?php echo htmlspecialchars($movie['imdb_rating']); ?>/10</p>
    </div>

    <!-- Section with similar movies -->
    <div class="similar-movies mt-12 mx-auto">
        <h2 class="text-2xl font-semibold text-neutral-100 mb-4">Similar Movies</h2>
        <div class="flex flex-wrap gap-6 mx-auto">
            <?php foreach ($similar_movies as $similar): ?>
                <a href="movie.php?id=<?php echo htmlspecialchars($similar['imdb_id']); ?>" class="flex flex-col bg-neutral-800 p-4 rounded-lg hover:bg-neutral-700 transition w-40">
                    <img src="<?php echo htmlspecialchars($similar['poster_url']); ?>" alt="<?php echo htmlspecialchars($similar['title']); ?>" class="h-32 object-cover rounded-md mb-2">
                    <h3 class="text-md font-semibold text-neutral-100"><?php echo htmlspecialchars($similar['title']); ?></h3>
                    <p class="text-sm text-neutral-400"><?php echo htmlspecialchars($similar['year']); ?></p>
                </a>
            <?php endforeach; ?>
        </div>
    </div>
</div>

</body>
</html>
