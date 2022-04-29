
const fields = Array.from(document.getElementsByClassName('input-field'))

const submitBtn = document.getElementById('submitButton')

const updateForm = ()=>{

    const values = fields.map(x => (({name, value}) => ({name, value}))(x));
    let isValid = values.every(x => x.value);

    submitBtn.disabled  = !isValid;

    return {isValid,values};
}

const initializeForm = () =>{
    console.log(fields)

    submitBtn.disabled = true;

    for(const field of fields){
        field.oninput = (e)=>{
            let {isValid, formValues} = updateForm();

            submitBtn.classList[isValid ? "remove" : "add"]("disabled")
            //if (isValid){
            //    submitBtn.classList.remove("disabled")
            //} else {
            //    submitBtn.classList.add("disabled")
            //}

            console.log(isValid)
        }
    }
}

initializeForm()