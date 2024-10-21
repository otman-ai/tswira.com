// SignInButton.js
import React from 'react';
import axios from "axios";
import { auth, provider, signInWithPopup } from '../authentification/firebase';
import { endpoints } from '../constants';

export function SignInButton ({setMessage, label, setSession}) {
  const handleSignIn = async () => {
    try {
      const result = await signInWithPopup(auth, provider);
      const token = await result.user.getIdToken();
      // Send the token to your Django backend
      const response = await axios.post(`${endpoints["login"]}`,{token:token}, {
        headers: {
          'Content-Type': 'application/json',
        },
      });
      localStorage.setItem("token", response.data["token"]);
      setSession(response.data["token"])
      setMessage({danger:false, message:"Login successfully"})
    } catch (erro) {
      console.error(erro);
      setMessage({danger:false, message:erro.response["data"]["message"]})

    }
  };

  return (
    <button onClick={handleSignIn} class="bg-white px-4 py-2 border flex gap-2 border-slate-200 dark:border-slate-700 rounded-lg text-slate-700 dark:text-slate-200 hover:border-slate-400 dark:hover:border-slate-500 hover:text-slate-900 dark:hover:text-slate-300 hover:shadow transition duration-150">
        <img class="w-6 h-6" src="https://www.svgrepo.com/show/475656/google-color.svg" loading="lazy" alt="google logo"/>
        <span className='text-black text-medium'>{label}</span>
    </button>
  );
};

