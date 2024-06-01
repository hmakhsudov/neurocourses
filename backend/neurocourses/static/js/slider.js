// slider.js

$(document).ready(function() {
    var $slider = $('.courses__slider');
    var $cards = $slider.find('.course__card');
    var cardWidth = $cards.outerWidth(true);
    var scrollAmount = cardWidth * 3; // Scroll by 3 cards at a time

    $slider.wrap('<div class="slider-wrapper"></div>');

    var $wrapper = $slider.parent();
    $wrapper.css({
        'position': 'relative',
        'overflow': 'hidden',
        'width': '100%'
    });

    $slider.css({
        'display': 'flex',
        'transition': 'transform 0.5s ease'
    });

    $wrapper.append($prevButton);
    $wrapper.append($nextButton);

    var maxScroll = $cards.length * cardWidth - $wrapper.width();
    var currentScroll = 0;

    $nextButton.click(function() {
        if (currentScroll < maxScroll) {
            currentScroll += scrollAmount;
            if (currentScroll > maxScroll) {
                currentScroll = maxScroll;
            }
            $slider.css('transform', 'translateX(-' + currentScroll + 'px)');
        }
    });

    $prevButton.click(function() {
        if (currentScroll > 0) {
            currentScroll -= scrollAmount;
            if (currentScroll < 0) {
                currentScroll = 0;
            }
            $slider.css('transform', 'translateX(-' + currentScroll + 'px)');
        }
    });
});
