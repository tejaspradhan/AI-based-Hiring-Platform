const signUpButton = document.getElementById('signUp');
const signInButton = document.getElementById('signIn');
const container = document.getElementById('container1');
const submitButton = document.getElementById('submit');

signUpButton.addEventListener('click', () => {
	container.classList.add("right-panel-active");

});

signInButton.addEventListener('click', () => {
	container.classList.remove("right-panel-active");
});