var showReviewsButton = document.querySelector('.show-reviews-button');
var reviewsList = document.querySelector('.feed-item-reviews');
showReviewsButton.addEventListener('click', function () {
	reviewsList.classList.toggle('reviews-hidden');
});
function updateSelectedUser(selectElement) {
	console.log(selectElement);
	// Get the selected option from the select element
	const selectedOption = selectElement.options[selectElement.selectedIndex];
	// Get the text content of the selected option (the username)
	const selectedUser = selectedOption.textContent;
	// Update the contents of the h1 element with the selected username
	document.getElementById('selected-user').textContent = selectedUser;
}
