
console.log('load Style')


// Share Btn
const viewBtn = document.getElementById('view-model')
const popup = document.querySelector(".pop")
const closeBtn = document.getElementById("close-btn")
const field = document.querySelector('.copy-field')
const inputCopy = document.getElementById('copy-text')
const btnCopy = document.getElementById('btn-copy')

var link = document.URL
inputCopy.value = link;

viewBtn.addEventListener('click', () => {
    popup.classList.toggle("show");
    console.log('i am here...')
})



closeBtn.onclick = ()=>{
    viewBtn.click();
}

btnCopy.addEventListener('click', () => {
     //select input value
    console.log(inputCopy.value);
    if(document.execCommand("copy")){ //if the selected text is copied
        field.classList.add('active');
        btnCopy.innerText = "Copied";
        navigator.clipboard.writeText(inputCopy.value);
        setTimeout(()=>{
            window.getSelection().removeAllRanges(); //remove selection from page
            field.classList.remove("active");
            btnCopy.innerText = "Copy";
        }, 3000);
    }
})


const replyBtn = document.getElementById('reply-btn')
const replyBox = document.querySelector('.reply-box')

replyBtn.addEventListener('click', () => {
    console.log('reply box')
    replyBox.classList.toggle('active');
})
