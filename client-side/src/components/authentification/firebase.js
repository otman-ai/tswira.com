// Import the functions you need from the SDKs you need
import { initializeApp } from "firebase/app";
import { getAnalytics } from "firebase/analytics";
import { getAuth, GoogleAuthProvider, signInWithPopup } from "firebase/auth";

// TODO: Add SDKs for Firebase products that you want to use
// https://firebase.google.com/docs/web/setup#available-libraries

// Your web app's Firebase configuration
// For Firebase JS SDK v7.20.0 and later, measurementId is optional
const firebaseConfig = {
  apiKey: "AIzaSyB20zBlnbv-IU5R-1dgiZlHIJiyhrcRa7Y",
  authDomain: "extended-arcana-380719.firebaseapp.com",
  projectId: "extended-arcana-380719",
  storageBucket: "extended-arcana-380719.appspot.com",
  messagingSenderId: "344159607352",
  appId: "1:344159607352:web:18fedfc4e2b00f916ae4cd",
  measurementId: "G-P5D9TQX8HM"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);
const analytics = getAnalytics(app);

const auth = getAuth(app);
const provider = new GoogleAuthProvider();
export { auth, provider, signInWithPopup ,analytics};
