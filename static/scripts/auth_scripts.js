
/** 
 * @summary Takes in an email and password and logins the user into the system if the details are valid.
 * 
 * @param {string} email - The user inputted email address they want to access.
 * @param {string} password -  The user inputted password connected to the email the inputted.
*/
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

            document.cookie = "name=" + emailPrefix

            location.reload()
        })
        .catch((error) => {
            const errorCode = error.code;
            const errorMessage = error.message;
        });
}

/** 
 * @summary Takes in an email and password and generates a user account from it, then logs the user into the system.
 * 
 * @param {string} email - The user inputted email address they want to use.
 * @param {string} password -  The user inputted password they want to use.
*/
function signup(email, password) {

    if (email != "" && password != "") {

        const auth = firebase.auth();
        auth.createUserWithEmailAndPassword(email, password)
            .then((userCredential) => {

                login(email, password);

            })
            .catch((error) => {
                const errorMessage = error.message;

                document.getElementById("registerErrorLabel").innerHTML = errorMessage
                document.getElementById("registerErrorContainer").style.display = "flex";

            });

    }
    else {

        if (email == "" && password == "") {

            document.getElementById("registerErrorLabel").innerHTML = " Please enter an Email and a Password."

        } else if (email == "") {

            document.getElementById("registerErrorLabel").innerHTML = "Please enter an Email."

        } else if (password == "") {

            document.getElementById("registerErrorLabel").innerHTML = "Please enter a Password."

        }

        document.getElementById("registerErrorContainer").style.display = "flex";

    }

}

/** 
 * @summary Logs the user out of the system and resets the pages cookies for the user.
*/
function logout() {

    const auth = firebase.auth();
    auth.signOut();
    
    document.cookie = "token="
    document.cookie = "name="
    location.href = "/";

}