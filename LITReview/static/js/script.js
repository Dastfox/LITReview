var showReviewsButton = document.querySelector('.show-reviews-button');
var reviewsList = document.querySelector('.feed-item-reviews');
showReviewsButton.addEventListener('click', function () {
	reviewsList.classList.toggle('reviews-hidden');
});
