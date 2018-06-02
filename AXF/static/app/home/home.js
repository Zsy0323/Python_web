$(function () {
    new Swiper ('.swiper-container', {
        // direction: 'vertical',
        loop: true,
        pagination: '.swiper-pagination',
    });

    //必购
    new Swiper('#swiperMenu', {
        slidesPerView: 3,
    });
});
