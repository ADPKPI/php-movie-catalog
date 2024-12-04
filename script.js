let page = 1;
let loading = false;

// Функціонал кнопки "Повернутися нагору"
const backToTop = document.getElementById('back-to-top');
window.addEventListener('scroll', () => {
    backToTop.style.display = window.scrollY > 200 ? 'block' : 'none';
});
backToTop.addEventListener('click', () => {
    window.scrollTo({ top: 0, behavior: 'smooth' });
});

// Обробка форми пошуку
document.getElementById('search-form').addEventListener('submit', (event) => {
    event.preventDefault();
    page = 1; // Скидання сторінки при новому пошуку
    document.getElementById("movie-container").innerHTML = ''; // Очищення контейнера з фільмами
    loadMovies(); // Завантаження фільмів з новими параметрами
});

// Асинхронне завантаження фільмів
async function loadMovies() {
    if (loading) return; // Перевірка, чи вже йде завантаження
    loading = true;
    document.getElementById("loading").style.display = "block"; // Відображення індикатора завантаження

    const formData = new FormData(document.getElementById('search-form'));
    const params = new URLSearchParams(formData);
    params.append('page', page);

    // Додаємо параметр сортування
    const sort = document.getElementById('sort').value;
    params.append('sort', sort);

    try {
        // Виконання запиту на сервер для отримання фільмів
        const response = await fetch(`fetch_movies.php?${params.toString()}`);
        const movies = await response.json();

        if (movies.length > 0) {
            const movieContainer = document.getElementById("movie-container");
            // Створення карток фільмів
            movies.forEach(movie => {
                const movieElement = document.createElement("div");
                movieElement.className = "flex flex-col bg-neutral-800 p-4 rounded-lg hover:bg-neutral-700 transition w-52 overflow-hidden movie-card";
                movieElement.innerHTML = `
                    <div class="w-full h-72 overflow-hidden rounded-md mb-2">
                        <img src="${movie.poster_url}" alt="${movie.title}" class="w-full h-full object-cover">
                    </div>
                    <h3 class="text-lg font-semibold text-neutral-100">${movie.title}</h3>
                    <p class="text-sm text-neutral-400">${movie.year}</p>
                `;
                movieElement.onclick = () => {
                    // Перехід на сторінку фільму
                    window.location.href = `movie.php?id=${movie.imdbID}`;
                };
                movieContainer.appendChild(movieElement);
                // Анімація для нових елементів
                setTimeout(() => movieElement.classList.add('loaded'), 100);
            });
            page++; // Переходимо до наступної сторінки
        } else {
            // Вимикаємо подію прокручування, якщо більше немає даних
            window.removeEventListener('scroll', handleScroll);
        }
    } catch (error) {
        console.error("Помилка під час завантаження фільмів:", error);
    } finally {
        loading = false;
        document.getElementById("loading").style.display = "none"; // Приховуємо індикатор завантаження
    }
}

// Обробка прокручування сторінки для автоматичного завантаження
function handleScroll() {
    if ((window.innerHeight + window.scrollY) >= document.body.offsetHeight - 100) {
        loadMovies();
    }
}

// Додаємо слухач прокручування сторінки
window.addEventListener('scroll', handleScroll);

// Початкове завантаження фільмів
loadMovies();
