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
    const auth = firebase.auth();
    auth.createUserWithEmailAndPassword(email, password)
      .then((userCredential) => {
        // Signed in 
        const user = userCredential.user;
        // ...
      })
      .catch((error) => {
        const errorCode = error.code;
        const errorMessage = error.message;
        // ..
      });
}

function logout(){
    const auth = firebase.auth();
    auth.signOut();
    document.cookie = "token="
    document.cookie = "name="
    location.href = "/";
}