const fields = Array.from(document.getElementsByClassName('input-field'))
const submitBtn = document.getElementById('submitButton')
const kavInput = document.getElementById('kav')
const currentStopInput = document.getElementById('current_stop')
const exitStopInput = document.getElementById('exit_stop')
const stopsDataset = document.getElementById('stops')

const updateForm = () => {

    const values = fields.map(x => (({name, value}) => ({name, value}))(x));
    let isValid = values.every(x => x.value);

    submitBtn.disabled = !isValid;

    return {isValid, values};
}

console.log(fields)
submitBtn.disabled = true;

kavInput.oninput = (e) => {
    let {isValid, formValues} = updateForm();
    isValid = isValid && !isNaN(kavInput.value)
    if (kavInput.value.length > 0 && !isNaN(kavInput.value)) {
        stopsDataset.innerHTML = ""
        fetch(encodeURI("/getstops?kav=" + kavInput.value))
            .then(response => response.json())
            .then(data => {
                for (const stop of data) {
                    let listitem = document.createElement("option")
                    listitem.textContent = stop
                    stopsDataset.appendChild(listitem);
                }
            })
    }
    submitBtn.classList[isValid ? "remove" : "add"]("disabled")
}

currentStopInput.oninput = (e) => {
    let {isValid, formValues} = updateForm();
    submitBtn.classList[isValid ? "remove" : "add"]("disabled")
}

exitStopInput.oninput = (e) => {
    let {isValid, formValues} = updateForm();
    submitBtn.classList[isValid ? "remove" : "add"]("disabled")
}