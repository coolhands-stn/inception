const predictedImage = document.getElementById("output-image");
const imageIndex = document.getElementById("image-index");

const imageName = parseInt(imageIndex.textContent);

if((imageName !== '') || (imageName !== null) ){
    predictedImage.src = `../static/frames/${imageName}.jpeg` ;
}

// Show predicted output button
showPredictedOutput = document.querySelector("nav p");

// Close predicted output button
const closeOutput = document.querySelector(".fa-bars-staggered");
// Frame wrap
const outputWrap = document.getElementById("output-wrap");

closeOutput.addEventListener("click", ()=> {
    outputWrap.style.display = "none";
});

showPredictedOutput.addEventListener("click", ()=> {
    outputWrap.style.display = "flex";
});