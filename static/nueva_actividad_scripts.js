const imgDiv1 = document.querySelector('.profile-pic-div1');
const img1 = document.querySelector('#photo1');
const file1 = document.querySelector('#file1');
const uploadBtn1 = document.querySelector('#uploadbtn1');

imgDiv1.addEventListener('mouseenter', function(){
    uploadBtn1.style.display = "block";
});

imgDiv1.addEventListener('mouseleave', function(){
    uploadBtn1.style.display = "none";
});

file1.addEventListener('change', function(){
    const choosedFile = this.files[0];
    if(choosedFile){
        const reader = new FileReader();

        reader.addEventListener('load',function(){
            img1.setAttribute('src',reader.result)
        });

        reader.readAsDataURL(choosedFile);


    }
});


//2
const imgDiv2 = document.querySelector('.profile-pic-div2');
const img2 = document.querySelector('#photo2');
const file2 = document.querySelector('#file2');
const uploadBtn2 = document.querySelector('#uploadbtn2');

imgDiv2.addEventListener('mouseenter', function(){
    uploadBtn2.style.display = "block";
});

imgDiv2.addEventListener('mouseleave', function(){
    uploadBtn2.style.display = "none";
});

file2.addEventListener('change', function(){
    const choosedFile = this.files[0];
    if(choosedFile){
        const reader = new FileReader();

        reader.addEventListener('load',function(){
            img2.setAttribute('src',reader.result)
        });

        reader.readAsDataURL(choosedFile);


    }
});


//3
const imgDiv3 = document.querySelector('.profile-pic-div3');
const img3 = document.querySelector('#photo3');
const file3 = document.querySelector('#file3');
const uploadBtn3 = document.querySelector('#uploadbtn3');

imgDiv3.addEventListener('mouseenter', function(){
    uploadBtn3.style.display = "block";
});

imgDiv3.addEventListener('mouseleave', function(){
    uploadBtn3.style.display = "none";
});

file3.addEventListener('change', function(){
    const choosedFile = this.files[0];
    if(choosedFile){
        const reader = new FileReader();

        reader.addEventListener('load',function(){
            img3.setAttribute('src',reader.result)
        });

        reader.readAsDataURL(choosedFile);


    }
});

//4
const imgDiv4 = document.querySelector('.profile-pic-div4');
const img4 = document.querySelector('#photo4');
const file4 = document.querySelector('#file4');
const uploadBtn4 = document.querySelector('#uploadbtn4');

imgDiv4.addEventListener('mouseenter', function(){
    uploadBtn4.style.display = "block";
});

imgDiv4.addEventListener('mouseleave', function(){
    uploadBtn4.style.display = "none";
});

file4.addEventListener('change', function(){
    const choosedFile = this.files[0];
    if(choosedFile){
        const reader = new FileReader();

        reader.addEventListener('load',function(){
            img4.setAttribute('src',reader.result)
        });

        reader.readAsDataURL(choosedFile);


    }
});