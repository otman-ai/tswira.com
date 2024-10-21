import './App.css'
import { SignInButton } from "./components/Buttons/GoogleSignUp"
import { useEffect, useState } from 'react';
import { getData } from './components/constants/functions';
import { DOMAIN, endpoints , examples} from './components/constants';
import axios from 'axios';
import { Menu, MenuButton, MenuItem, MenuItems } from '@headlessui/react'
import { ChevronDownIcon } from '@heroicons/react/20/solid';
import * as React from 'react';
import { Analytics } from "@vercel/analytics/react"



const ImageTransformer = ({ images }) => {
    const [transformedImage, setTransformedImage] = useState(null);

    const handleTransformImages = () => {
        // Logic to transform images into one image
        // For demonstration, we'll just take the first image
        if (images.length > 0) {
            setTransformedImage(images.slice(4, images.length)); // Replace with actual transformation logic
        }
    };

    return (
        <div className="image-transformer flex lg:flex-row flex-col lg:space-y-0 lg:gap-4 lg:p-10 lg:h-fit space-y-4 items-center justify-center rounded-lg p-4">
            <div className="image-group">
                <img key={0} src={images[0]} className="w-full h-64 rounded-lg" />
            </div>
            <div className="arrow-container flex items-center justify-center" onMouseEnter={handleTransformImages}>
                <span className="arrow text-2xl">➡️</span> {/* Arrow to indicate transformation */}
            </div>

                <div className="grid grid-cols-3  lg:grid-cols-5 gap-2">
                    {images.slice(1, images.length).map((image, index) => (
                        <img key={index} src={image} alt={`Image ${index + 1}`} className="w-full h-24 object-cover rounded-lg" />
                    ))}
                </div>
            
        </div>
    );
};

const UniquePrompts = ({ Generated }) => {
    // Check if Generated exists and has elements
    if (!Generated || Generated.length === 0) {
        return null; // Return null instead of undefined
    }

// Extract unique job_ids
const uniqueJobIds = Array.from(new Set(Generated.map(item => item.job_id)));

// Extract unique prompts
const uniquePrompts = uniqueJobIds.map(job_id => {
    // Get the first occurrence of the job_id
    return Generated.find(item => item.job_id === job_id);
});


    return (
        <div className="w-full flex  flex-wrap gap-3 grid grid-cols-4">
            {uniquePrompts.sort((a, b) => new Date(b.created_at) - new Date(a.created_at)).map((item) => (
                <a href={`/?job_id=${item.job_id}`} className="p-3 hover:bg-[#4F4242] bg-[#231313]  items-center rounded-lg shadow-lg" key={item.id}>
                    {/* Image display */}
                    <img 
                        src={item.image} // Make sure the image URL is available in your data
                        alt={item.prompt} 
                        className="w-full lg:h-50 object-cover rounded-lg"
                    />
                    <div className="text-start mt-4">
                        <h3 className=" font-semibold truncate text-lg text-gray-100">{item.prompt}</h3>
                        <p className=" text-sm text-gray-300">{item.style_name}</p>
                        <p className=" text-sm text-gray-400"> {item.num_outputs} Images</p>
                    </div>
                </a>
            ))}
        </div>
    );
};


function PricingPage({client_secret, IsOpen, setIsOpen}) {
  if(!IsOpen){
    return ;
  }
  return (
<div className="fixed inset-0 z-50 flex items-center justify-center bg-black bg-opacity-50" onClick={()=>setIsOpen(false)}>
  <div 
    className="relative bg-[#231313]  w-full max-w-[50%] lg:px-12 lg:py-12 max-h-[80%] rounded-lg shadow-lg overflow-y-auto" 
    onClick={(e) => e.stopPropagation()} // To prevent closing when clicking inside
  >
    <button 
      className="absolute top-1 right-3 text-[30px] text-gray-700 hover:text-red-500 transition-all" 
      onClick={()=>setIsOpen(false)}
    >
      &times;
    </button>

    <div className="w-full h-auto">
      <stripe-pricing-table
        pricing-table-id={import.meta.env.VITE_PRICING_TABLE_ID}
        publishable-key={import.meta.env.VITE_PUBLISHABLE_KEY}
        customer-session-client-secret={client_secret}
      />
    </div>
  </div>
</div>

    
  );

}


function DropDownProfile({UserData, setIsOpen, handleSubscription}) {
  return (
    <Menu as="div" className="relative inline-block text-left space-y-2">
      <div>
        <MenuButton className="">
        <img src={UserData?.profile} className='cursor-pointer rounded-full w-12 h-12  bg-[#130202] p-1 bg-cover ' title={UserData?.name} alt="" />
        {/* <ChevronDownIcon aria-hidden="true" className="-mr-1 h-5 w-5 text-gray-400" /> */}
        </MenuButton>
      </div>

      <MenuItems
        transition
        className="p-2 absolute right-0 z-10 w-56 origin-top-right rounded-md bg-[#130202] shadow-lg ring-1 ring-black ring-opacity-5 transition focus:outline-none data-[closed]:scale-95 data-[closed]:transform data-[closed]:opacity-0 data-[enter]:duration-100 data-[leave]:duration-75 data-[enter]:ease-out data-[leave]:ease-in"
      >
        <div className='text-gray-100 py-2 text-base space-y-2'>
          <p>{UserData?.user}</p>
          <p className='text-gray-300'>{UserData?.email}</p>
          <p className='text-yellow-300'>{UserData?.subscription.plan.toUpperCase()}</p>

        </div>

        <div className="py-2">
          {UserData?.subscription.plan.toLowerCase() !== "free"?
          <MenuItem className="w-full flex justify-center">
          <button onClick={()=> handleSubscription()}
	    className="mb-2 bg-gradient-to-r from-[#229F2B] to-[#822727] text-white font-semibold py-2 px-4 rounded-lg transition duration-300 ease-in-out transform hover:scale-110">
         My subscription
        </button>
          </MenuItem>:<MenuItem>
          <button onClick={()=> setIsOpen(true)}
	    className="mb-2 bg-gradient-to-r from-[#229F2B] to-[#822727] text-white font-semibold py-2 px-4 rounded-lg transition duration-300 ease-in-out transform hover:scale-110">
         Upgrade plan
        </button>
          </MenuItem>}
          <MenuItem>
            <a
              href="/"
              className="block px-4 py-2  text-gray-100 data-[focus]:bg-[#231313]"
            >
              Prompts
            </a>
          </MenuItem>
            <MenuItem>
              <button
                className="block w-full px-4 py-2 text-left  text-red-400 data-[focus]:bg-[#231313]"
                onClick={()=>{
                  localStorage.removeItem("token");
                  window.location.href = import.meta.env.VITE_DOMAIN; // Redirect to DOMAIN
                  ;}}
              >
                Sign out
              </button>
            </MenuItem>
        </div>
      </MenuItems>
    </Menu>
  )
}
const Slider = ({value, onChange}) => {
  // const [value, setValue] = useState(50); // Default slider value

  return (
      <div className="w-full max-w-md space-y-2">
        <label htmlFor="user-input" className="block text-lg font-medium text-gray-200 mb-2">
          Number of Images
        </label>
        <p className='text-gray-400'>Number of the outputs</p>

        <div className="flex items-center justify-between">
          <input
            id="slider"
            name='num_outputs'
            type="range"
            min="1"
            max="100"
            value={value}
            onChange={onChange}
            style={{
              background: `linear-gradient(to right, #23751C ${value}%, #130202 ${value}%)`,
            }}
            className="w-full h-2 bg-[#130202] rounded-lg appearance-none outline-none"
          />
          <span className="text-gray-200 pl-3">{value}</span>
        </div>
        
      </div>
  );
};

const DropdownSelect = ({value, onChange}) => {
  const options = ["Photographic (Default)", "Cinematic", "Disney Charactor", 
                  "Digital Art", "Fantasy art", "Neonpunk", "Enhance", "Lowpoly",
                   "Comic book", "Line art"];

  return (
      <div className="w-full max-w-md space-y-2">
        <label htmlFor="user-input" className="block text-lg font-medium text-gray-200 mb-2">
            Styles
        </label>
        <p className='text-gray-400'>Which style you want to use to generate the images</p>

        <div className="relative">
          <select
            id="dropdown"
            name="style_name"
            value={value}
            onChange={onChange}
            className="block appearance-none w-full bg-[#130202] border border-[#144210] outline-none text-gray-50 py-3 px-4 pr-8 rounded-lg shadow-sm focus:border-[#23751C] focus:ring-2"
          >
            <option value="" disabled>Select style</option>
            {options.map((option, index) => (
              <option key={index} value={option}>
                {option}
              </option>
            ))}
          </select>
          <div className="absolute inset-y-0 right-0 flex items-center px-2 pointer-events-none">
            <svg className="w-4 h-4 text-gray-500" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M19 9l-7 7-7-7"></path>
            </svg>
          </div>
        </div>
      </div>

  );
};

const ImageView = ({ selectedImage, onClose }) => {
  if (!selectedImage) return null;

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center" onClick={onClose}>
      <div className="relative max-w-4xl p-4 rounded-lg" onClick={(e) => e.stopPropagation()}>
        <div className='p-10'>
          <img src={selectedImage} alt="Selected Image" className="w-full h-auto object-cover rounded-lg max-h-screen my-4"/>

<a 
          href={selectedImage} 
          download="image.jpg" 
          className="absolute top-16 right-12 underline text-white text-lg px-4 py-2 rounded-lg">
          Download
        </a>
        </div>

        <button className="absolute top-4 right-2 text-[30px] text-white" onClick={onClose}>
          &times;
        </button>

        {/* Download button */}
        
      </div>
    </div>
  );
};



const ImageUpload = ({setFormData, Form_Data}) => {
  const [selectedImages, setSelectedImages] = useState([]);
  const [uploadedImages, setUploadedImages] = useState(null); // State to store uploaded images
  const [selectedImage, setSelectedImage] = useState(null); // State to keep track of the selected image
  const session = localStorage.getItem("token") // Replace with your actual token


  const [isExpanded, setIsExpanded] = useState(false); // State to manage expanded view
  const [isLoading, setIsLoading] = useState(false); // State to manage loading status
  const [Error, setError] = useState(false); // State to manage loading status

  useEffect(()=>{

  }, [session])

  const handleExpandImages = () => {
    setIsExpanded(!isExpanded); // Toggle expanded state
  };
  // Function to fetch uploaded images
  const fetchUploadedImages = async () => {
    try {
      const response = await axios.get(endpoints["images"], {
        headers: {
          "Authorization": `Token ${session}`, // Include the token in the headers
        },
      });
      // setUploadedImages(response.data.images); // Assuming the response structure matches
      setUploadedImages(response.data.images);
      console.log(response.data.images)
    } catch (error) {
      console.error('Error fetching images:', error);
      setError(error.response.data["message"])
    }
  };

  useEffect(() => {
    if(session){
    fetchUploadedImages(); // Fetch images on component mount
  }}, [session]);

  const handleSelectImage = (index) => {
    const image = uploadedImages[index].image;
    
    setFormData((prevData) => {
      const isSelected = prevData.selectedImages.includes(image);
      return {
        ...prevData,
        selectedImages: isSelected
          ? prevData.selectedImages.filter((url) => url !== image) // Remove the image if it's already selected
          : [...prevData.selectedImages, image], // Add the image if it's not selected
      };
    });
  };

  const uploadImage = async (image) => {
    
    console.log("Uploading...", image)
    const formData = new FormData();
    formData.append('image', image.file); // Append the image file to the form data
    console.log(formData)
    try {
      const response = await axios.post(endpoints["upload_image"], formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
          'Authorization': `Token ${session}`, // Include the token in the headers
        },
      });
      console.log('Upload successful:', response.data);
    } catch (error) {
      console.error('Error uploading image:', error);
    }
  };

  const handleImagesChange = async (e) => {
    if(!session){
      setError("You need to login to use the app");
      return ;
    }
    setError(null)
    setIsLoading(true)
    const files = Array.from(e.target.files);
    const newImages = files.map((file) => ({
      file,
      preview: URL.createObjectURL(file), // Create a preview URL for each image
    }));


    // Upload each image one by one
    for (const image of newImages) {
      await uploadImage(image); // Call the upload function for each image
    }
    fetchUploadedImages()
    setIsLoading(false)
  };


  return (
    <div className="space-y-2">
      <label htmlFor="user-input" className="block text-lg font-medium text-gray-200 mb-2">
        Input Images
      </label>
      <p className='text-gray-400'>Upload the images you want to use as source (SUPPORT ONLY PNG, JPG and JPEG)</p>
      <div className="flex items-center justify-center w-full h-12 bg-[#130202] border-2 border-dashed border-gray-400 rounded-lg mb-4">
        <label className="cursor-pointer">
          <span className="text-gray-200">Click to upload</span>
          <input
            type="file"
            accept="image/*"
            multiple 
            onChange={handleImagesChange}
            className="hidden"
          />
        </label>
      </div>
      <p className='text-red-500'>{Error}</p>
      {isLoading && (
        <div className="flex items-center justify-center">
          <svg className="animate-spin h-5 w-5 text-gray-200" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
            <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
            <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8v2a6 6 0 100 12v2a8 8 0 01-8-8z"></path>
          </svg>
          <span className="ml-2 text-gray-200">Uploading...</span>
        </div>
      )}
      {uploadedImages && <>
            <p className='text-gray-400 text-center w-full text-sm'>Or</p>

      <div className="relative bg-[#130202] p-2 space-y-3 rounded-lg hover:bg-[#130202]/90">
          <button onClick={handleExpandImages} className="flex items-center text-gray-200  w-full ">
            {isExpanded ? (
              <svg xmlns="http://www.w3.org/2000/svg" className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
              </svg>
            ) : (
              <svg xmlns="http://www.w3.org/2000/svg" className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 15l7-7 7 7" />
              </svg>
            )}
            <span className="ml-2">Uploaded images</span>
          </button>
          
          {isExpanded && (
            <div className="grid grid-cols-2 gap-4 mt-2">
              {uploadedImages.map((image, index) => {
                  const isSelected = Form_Data.selectedImages.includes(image.image); // Check if the image is selected
                  return (
                    <div key={image.id} className={`p-2 relative ${isSelected ? 'bg-[#231313]  rounded-lg' : 'bg-transparent'}`}> {/* Change background color based on selection */}
                      <img
                        src={image.image_url}
                        alt="Uploaded"
                        className="w-full h-32 object-cover rounded-lg cursor-pointer"
                        onClick={() => handleSelectImage(index)} // Adjust as needed
                      />
                    </div>)
})}
            </div>
          )}
        </div></>}
    </div>
  );
};

function App() {
  const token  = localStorage.getItem("token"); 
  // "b8787d8aab2f643d7750cd7f96b42b87819cd55f"
  const [message, setMessage] = useState()
  const [selectedImage, setSelectedImage] = useState(null); // State to keep track of the selected image
  const [UserData, setUserData] = useState(null); // State to keep track of the selected image
  const [isGenerating, setIsGenerating] = useState(null); // State to keep track of the selected image
  const [Generated, setGenerated] = useState([]);
  const [session, setSession] = useState(token); // State to manage expanded view
  const [IsOpen, setIsOpen] = useState(false); // State to manage expanded view

  const [formData, setFormData] = useState({
    prompt: '',
    num_outputs: 1, // Default number of outputs
    style_name: '', // Selected style
    selectedImages: [], // Array to hold selected images
  });
  const [jobId, setjobId] = useState(false); // State to manage loading status
  useEffect(() => {
    const params = new URLSearchParams(window.location.search);
    const job_id = params.get('job_id');
    if (job_id) {
      setjobId(job_id);
      const checkStatus = setInterval(() => {
        getData(endpoints["photo_status"] + "/?job_id=" + job_id, session).then(response => {
          console.log("response: ", response)
          if(response.length === 0){
            clearInterval(checkStatus)
            return;
          }else{
        setGenerated(response);
        const firstGenerated = response[0];
        setFormData(prevData => ({
          ...prevData,
          prompt: firstGenerated.prompt,
          style_name:firstGenerated.style_name,
          num_outputs: firstGenerated.num_outputs
        }));
          const allFinished = response.every(item => item.status === 'finish' || item.status === 'error');
          if (allFinished) {
            clearInterval(checkStatus);
          }
        }});
      }, 5000);
    }
  // useEffect(() => {
  //   if (job_id && Generated && Generated.length > 0) {
  //     const firstGenerated = Generated[0];
  //     setFormData(prevData => ({
  //       ...prevData,
  //       prompt: firstGenerated.prompt,
  //       num_outputs: firstGenerated.num_outputs,
  //       selectedImages: firstGenerated.input_images,
  //     }));
  //   }
  // }, [job_id]);


  }, []);
const get_photos = async()=>{
 try {
      const response = await axios.get(endpoints["photos"], {
        headers: {
          'Authorization': `Token ${session}`
        }
      });
      if (response.data) {
        console.log("Photos:", response.data);
        setGenerated(response.data)
      } else {
        console.error("No data found");
      }
    } catch (error) {
      console.error('Error:', error);
    }
} 
useEffect(()=>{
   if(!jobId && token){
	get_photos()
}
}, [token, jobId])
  const handleSubscription = async() =>{
	 try {
      const response = await axios.get(endpoints["billing"], {
        headers: {
          'Authorization': `Token ${session}`
        }
      });
      if (response.data.url) {
        window.location.href = response.data.url;
      } else {
        console.error("No url found");
      }
    } catch (error) {
      console.error('Error:', error);
    }
}
  const handleInputChange = (e) => {
    const { name, value } = e.target;
    if(name === "num_outputs"){
      setFormData((prevData) => ({
        ...prevData,
        [name]: parseInt(value),
      }));
    }else{
    setFormData((prevData) => ({
      ...prevData,
      [name]: value,
    }));
  }
  };
  const handleGenerateImage = async () => {
    if(!session){
      setMessage("You need to Login to use the app");
      return ;
    }
    setIsGenerating(true)
    setMessage(null)
    console.log(formData)

    try {
      const response = await axios.post(endpoints["create"], formData, {
        headers: {
          'Authorization': `Token ${session}`
        }
      });
      if (response.data.job_id) {
        window.location.href = `/?job_id=${response.data.job_id}`;
        // navigate(`/?job_id=${response.data.job_id}`)
      } else {
        console.error('Job ID not received');
      }
    } catch (error) {
      console.error('Error generating image:', error);
      setMessage(error.response.data["message"])
    }
    setIsGenerating(false)

  };

  useEffect(()=>{
    if(session){
      getData(endpoints["user_data"], session).then(response =>{
        setUserData(response)
        console.log(response)
      })
    }
  }, [session])
  const handleSelectImage = (index) => {
    setSelectedImage(Generated[index].image);
  };
  // const headerComponent = session ? <p className='text-gray-50'>{UserData?.features ? UserData.features.token_limits : 'Loading...'}</p> : <SignInButton label="Continue with Google" setMessage={setMessage}/>  ;
  const headerComponent = session ? (
    UserData ? (
      <div className="flex space-x-3 items-center justify-center">
        {UserData?.subscription?.plan?.toLowerCase() !== 'free' && (
          <p className='text-green-300 text-center items-center font-semibold'>{UserData?.subscription?.plan.toUpperCase()}</p>
        )}
        {UserData?.subscription?.plan?.toLowerCase() === 'free' && (
          <button 
          onClick={()=>setIsOpen(true)}
          className="bg-gradient-to-r from-[#229F2B] to-[#822727] text-white font-semibold py-2 px-4 rounded-lg transition duration-300 ease-in-out transform hover:scale-110">
         Upgrade plan
        </button>
        )}
        <div className="items-center space-x-1 flex">
          <span className='text-gray-50 text-center items-center font-semibold'>{UserData?.feature.token_limits - UserData?.feature.tokens}</span>
          <svg xmlns="http://www.w3.org/2000/svg" className="w-6 h-6" viewBox="0 0 24 24" fill="none" stroke="currentColor">
            <circle cx="12" cy="12" r="10" stroke="#fff" strokeWidth="2" />
            <text x="12" y="16" textAnchor="middle" fill="#fff" stroke='none' fontSize="10" fontWeight="bold">$</text>
          </svg>
        </div>
        <div className=''>
        <DropDownProfile UserData={UserData} setIsOpen={setIsOpen} handleSubscription={handleSubscription}/>
        {/* <img title={UserData["user"]} className='cursor-pointer rounded-full w-12 h-12  bg-[#130202] p-1 bg-cover ' src={UserData["profile"]} alt="" /> */}
        </div>
      </div>
      
    ) : (
      <div className="flex items-center justify-center space-y-2">
        <p className='text-gray-50'>Loading...</p>
      </div>
    )
  ) : (
    <SignInButton label="Continue with Google" setSession={setSession} />
  );

  return (<div className="bg-[#130202] w-full lg:h-screen lg:overflow-y-hidden">
    
  <PricingPage client_secret={UserData?.client_secret} setIsOpen={setIsOpen} IsOpen={IsOpen} />
  
  <header className="lg:p-9 p-3 bg-gradient-to-r from-[#0E2203] to-[#2F1919] h-[8%] w-full border-b border-b-2 border-gray-500">
    <div className='flex justify-between items-center h-full'>
      <div className='flex space-x-2'>
        <svg xmlns="http://www.w3.org/2000/svg" xmlnsXlink="http://www.w3.org/1999/xlink" width="40.207" height="30.544" viewBox="0 0 46.207 35.544">
          <defs>
            <linearGradient id="linear-gradient" x1="-0.11" y1="1.122" x2="1" y2="1.268" gradientUnits="objectBoundingBox">
              <stop offset="0" stopColor="#168900" />
              <stop offset="1" stopColor="#fe4242" />
            </linearGradient>
          </defs>
          <g id="layer1" transform="translate(-5.103 -7.618)">
            <g id="g2413" transform="translate(5.103 7.618)">
              <path id="path1848" d="M57.517,197.879c-1.969,0-2.674,1.793-3.554,3.554l-1.777,3.554H45.077a5.32,5.32,0,0,0-5.332,5.332v17.772a5.32,5.32,0,0,0,5.332,5.332H80.621a5.32,5.32,0,0,0,5.332-5.332V210.319a5.32,5.32,0,0,0-5.332-5.332H73.512l-1.777-3.554c-.889-1.777-1.585-3.554-3.554-3.554Z" transform="translate(-39.745 -197.879)" fill="url(#linear-gradient)" />
              <circle id="path2351" cx="1.852" cy="1.852" r="1.852" transform="translate(3.181 10.348)" fill="rgba(255,255,255,0.65)" />
              <path id="path2405" d="M60.818,207.271a9.35,9.35,0,1,0,9.353,9.346A9.352,9.352,0,0,0,60.818,207.271Zm0,4.952a4.4,4.4,0,1,1-4.4,4.4A4.4,4.4,0,0,1,60.818,212.223Z" transform="translate(-37.131 -195.784)" fill="rgba(255,255,255,0.65)" />
            </g>
          </g>
        </svg>
      </div>
      
      <div className='flex items-center space-x-4'>
        {headerComponent}
      </div>
    </div>
  </header>
{!token ? <ImageTransformer images={examples}/>:<section className="lg:flex lg:h-[90%] w-full">
    <div className="lg:w-[80%] p-3 lg:overflow-y-auto">
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
      {/* {!token && Generated.length === 0 ? examples.map((item, index) => (<div key={index} className="bg-gray-300 rounded-lg shadow-md cursor-pointer" onClick={() => handleSelectImage(index)}>
          <img 
            src={item}
            className="w-full h-full object-cover rounded-lg"
            loading="lazy"
            alt={`Generated image ${index + 1}`} // Added alt text for accessibility
          /></div>)):<>{!token && <div className="flex justify-center items-center text-center text-gray-50 w-full h-full">No Images yet</div>}</>} */}

  {jobId && Generated && Generated.length > 0 &&(

    Generated.map((item, index) => (
      <div key={item.id} className="bg-gray-300 rounded-lg shadow-md cursor-pointer" onClick={() => handleSelectImage(index)}>
        {item.status === "finish" ? (
          <img 
            src={item.image}
            className="w-full h-full object-cover rounded-lg"
            loading="lazy"
            alt={`Generated image ${index + 1}`} // Added alt text for accessibility
          />
        ) : item.status === "error" ? (
          <div className="bg-[#231313] rounded-lg shadow-md h-[399px] flex items-center justify-center">
            <span className="text-red-400">Error Generating the image</span>
          </div>
        ) : <div className="bg-[#231313] space-x-2 rounded-lg shadow-md h-[399px] flex items-center justify-center">
          <svg className="animate-spin h-5 w-5 text-gray-200" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
            <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
            <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8v2a6 6 0 100 12v2a8 8 0 01-8-8z"></path>
          </svg>
            <span className="text-gray-100">{item.status}</span>
          </div>
}
      </div>
    ))
  )}

</div>
{!jobId && <UniquePrompts Generated={Generated} />}
    </div>

    <div className="lg:w-[30%] bg-[#231313] p-3 lg:overflow-y-auto">
      <div className="p-4 space-y-4">
        <div>
          <label htmlFor="user-input" className="block text-lg font-medium text-gray-200 mb-2">
            Prompt
          </label>
          <textarea
            name="prompt"
            value={formData.prompt}
            onChange={handleInputChange}
            className='bg-[#130202] w-full h-fit min-h-16 p-2 text-gray-50 border border-[#144210] rounded-lg text-white outline-none focus:border-[#23751C] focus:ring-2'
            placeholder='A photo of a man walking in New York streets'
          />
        </div>

        <DropdownSelect
          value={formData.style_name}
          onChange={handleInputChange}
        />

        <Slider
          value={formData.num_outputs}
          onChange={handleInputChange}
        />

        <ImageUpload 
          Form_Data={formData}
          setFormData={setFormData}
          // onChange={handleImagesChange}
        />

        <p className="text-red-400">{message}</p>
        
        <button className="bg-gradient-to-r from-[#822727] to-[#229F2B] text-white font-semibold py-2 px-4 rounded-lg transition duration-300 ease-in-out transform hover:scale-110"
          onClick={() => handleGenerateImage()}>
          {isGenerating ? "Generating..." : "Generate Image"}
        </button>
      </div>


      <ImageView selectedImage={selectedImage} onClose={() => setSelectedImage(null)} />
    </div>
  </section>}


<Analytics />
</div>)}


export default App;
