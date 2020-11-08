let base_url = "http://127.0.0.1:8000"; //McDefect Solution API

function doPost(url, content_type, body, callback){
    var xmlHttp = new XMLHttpRequest();
    xmlHttp.onreadystatechange = function() { 
        if (xmlHttp.readyState == 4 && xmlHttp.status == 200)
            callback(xmlHttp.responseText);
    }
    xmlHttp.open("POST", url); // true for asynchronous 
    // xmlHttp.setRequestHeader('Content-type', content_type);

    // xmlHttp.setRequestHeader('Access-Control-Allow-Headers', '*');
    // xmlHttp.setRequestHeader('Access-Control-Allow-Origin', '*');
    // xmlHttp.setRequestHeader('Access-Control-Allow-Methods', 'POST');
    xmlHttp.send(body);
}


function detectDefect() {
    document.getElementById('detect-result-div').style.display = "none";
    document.getElementById('detect-spinner').style.display = "block";
    
    var img = document.getElementById('def-det-img').files[0];

    document.getElementById('detect-orig-img').src = URL.createObjectURL(img);

    let formData = new FormData()
    formData.append('img', img)

    doPost(base_url + "/detect/", "multipart/form-data", formData, (res) => {
        res = JSON.parse(res);
        console.log(res);
        var image = document.getElementById('detect-result-img');
        image.src = 'data:'+ res.mime + ';base64,' + res.image;
        document.getElementById('detect-spinner').style.display = "none";
        document.getElementById('detect-result-div').style.display = "block";
    })
}

function categorizeDefect() {
    document.getElementById('categorize-result-div').style.display = "none";
    document.getElementById('categorize-spinner').style.display = "block";
    
    var img = document.getElementById('def-cat-img').files[0];

    let formData = new FormData()
    formData.append('img', img)

    doPost(base_url + "/classify/", "multipart/form-data", formData, (res) => {
        res = JSON.parse(res);
        console.log(res);
        document.getElementById('categorize-result-div').innerHTML = `
            <h5>Prediction: ${res.prediction}</h5>
            <img src= ${URL.createObjectURL(img)}>
        `
        document.getElementById('categorize-spinner').style.display = "none";
        document.getElementById('categorize-result-div').style.display = "block";
    })
}