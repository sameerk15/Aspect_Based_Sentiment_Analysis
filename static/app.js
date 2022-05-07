const message = document.querySelector('#message');
const aspect = document.querySelector('#aspect');
const predict = document.querySelector('#predict');
const resultDiv = document.querySelector('#prediction');
const backendURL = 'http://localhost:5000/predict';

predict.addEventListener('click', predictSentiment);

function predictSentiment(e) {
	e.preventDefault();

	var myHeaders = new Headers();
	myHeaders.append('Content-Type', 'application/json');

	var raw = JSON.stringify({
		message: message.value,
		aspect: aspect.value,
	});

	var requestOptions = {
		method: 'POST',
		headers: myHeaders,
		body: raw,
		redirect: 'follow',
	};

	fetch(backendURL, requestOptions)
		.then((response) => response.json())
		.then((result) => {
			resultDiv.classList.remove('d-none');

			if (parseInt(result.code) === -1) resultDiv.classList.add('bg-error');
			else if (parseInt(result.code) === 0)
				resultDiv.classList.add('bg-primary');
			else resultDiv.classList.add('bg-success');

			resultDiv.innerHTML = result.summary;
		})
		.catch((error) => console.log('error', error));
}
