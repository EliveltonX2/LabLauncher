// Carrossel 1: Hero (Efeito Fade)
const swiper = new Swiper('.hero-swiper', {
    // Efeito de FADE (esmaecer)
    effect: 'fade',
    fadeEffect: {
        crossFade: true // Permite um fade mais suave
    },
    
    // Autoplay (troca sozinho)
    autoplay: {
        delay: 3000, // 3 segundos
        disableOnInteraction: false, // Continua mesmo se o usuário mexer
    },

    // Loop
    loop: true,

    // Remove setas e paginação (opcional)
    navigation: false,
    pagination: false,
});


const templatesSwiper = new Swiper('.templates-swiper', {
    // 1. ATIVAR O EFEITO COVERFLOW
    effect: 'coverflow',
    
    // 2. Centralizar o slide ativo (essencial para coverflow)
    centeredSlides: true,

    // 3. Loop
    loop: true,

    // 4. Quantos slides de uma vez (começar com 1 para mobile)
    slidesPerView: 1.5, // 1 slide central e metade dos laterais no celular
    
    // 5. Configurações do Coverflow
    coverflowEffect: {
        rotate: 40,      // Rotação dos slides laterais (em graus)
        stretch: 0,      // "Esticar" os slides (0 = sem esticar)
        depth: 100,      // Profundidade do eixo Z (quão "longe" os slides vão)
        modifier: 1,     // Multiplicador do efeito (1 = padrão)
        slideShadows: false, // Desativa as sombras padrão do swiper (vamos usar a nossa)
    },

    // Paginação (bolinhas)
    pagination: {
        el: '.swiper-pagination',
        clickable: true,
    },

    // Navegação (setas)
    navigation: {
        nextEl: '.swiper-button-next',
        prevEl: '.swiper-button-prev',
    },

    // Responsividade (Breakpoints)
    breakpoints: {
        // quando a tela for >= 768px (tablet)
        768: {
            slidesPerView: 2,
        },
        // quando a tela for >= 1024px (desktop)
        1024: {
            slidesPerView: 3, // Mostra 3 slides (1 centro, 2 laterais)
        },
    },
});