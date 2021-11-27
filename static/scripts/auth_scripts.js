function login(email, password) {
    const auth = firebase.auth();
    auth.signInWithEmailAndPassword(email, password)
    .then((userCredential) => {
        // Signed in 
        const user = userCredential.user;   

        document.cookie = "token=" + user['uid'];

        var email = user['email'];
        const emailSplit = email.split("@");
        const emailPrefix = emailSplit[0]

        console.log(name)

        document.cookie = "name=" + emailPrefix

        location.reload()
    })
    .catch((error) => {
        const errorCode = error.code;
        const errorMessage = error.message;
    });
}

function signup(email, password){

    

    if(email != "" && password != ""){

        const auth = firebase.auth();
        auth.createUserWithEmailAndPassword(email, password)
        .then((userCredential) => {
            
            login(email, password);

        })
        .catch((error) => {
            const errorCode = error.code;
            const errorMessage = error.message;

            document.getElementById("registerErrorLabel").innerHTML = errorMessage
            document.getElementById("registerErrorContainer").style.display = "flex";

        });

    }
    else{

        console.log("Yo")

        if(email == "" && password == ""){

            // Please put info error "no inputs"
            document.getElementById("registerErrorLabel").innerHTML = " Please enter an Email and a Password."

        }else if(email == ""){

            // Please put info error "no email"
            document.getElementById("registerErrorLabel").innerHTML = "Please enter an Email."

        }else if(password == ""){

            // Please put info error "no password"
            document.getElementById("registerErrorLabel").innerHTML = "Please enter a Password."

        }

        document.getElementById("registerErrorContainer").style.display = "flex";

    }

}

function logout(){
    const auth = firebase.auth();
    auth.signOut();
    document.cookie = "token="
    document.cookie = "name="
    location.href = "/";
}