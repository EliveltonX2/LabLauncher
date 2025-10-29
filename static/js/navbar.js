const navToggle = document.querySelector('.nav-toggle');
const navLinks = document.querySelector('.nav-links');

// 2. Adiciona o "ouvidor" de clique no botão
navToggle.addEventListener('click', () => {
    // 3. Adiciona/Remove a classe 'active' nos dois elementos
    navToggle.classList.toggle('active');
    navLinks.classList.toggle('active');
});

// Opcional: Fechar o menu ao clicar em um link
navLinks.querySelectorAll('a').forEach(link => {
    link.addEventListener('click', () => {
        navToggle.classList.remove('active');
        navLinks.classList.remove('active');
    });
});