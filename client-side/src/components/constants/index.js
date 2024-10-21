export const BASE_API = import.meta.env.VITE_BASE_API
export const DOMAIN = import.meta.env.DOMAIN
export const examples = [
"https://i.pinimg.com/originals/f3/d9/0c/f3d90c24cecfcacaf1dccda173d10b60.jpg",
"https://uploadedvideosyoutube.s3.eu-north-1.amazonaws.com/generated/0a21340a-d134-427b-b99e-eab0c1375996/image_2.png" ,

"https://uploadedvideosyoutube.s3.eu-north-1.amazonaws.com/generated/0a21340a-d134-427b-b99e-eab0c1375996/image_3.png",
 "https://uploadedvideosyoutube.s3.eu-north-1.amazonaws.com/generated/e7f7d437-b341-4d95-a2a7-01c9bfda770e/image_0.png", 
 "https://uploadedvideosyoutube.s3.eu-north-1.amazonaws.com/generated/0a21340a-d134-427b-b99e-eab0c1375996/image_1.png",

 "https://uploadedvideosyoutube.s3.eu-north-1.amazonaws.com/generated/e7f7d437-b341-4d95-a2a7-01c9bfda770e/image_2.png", 
"https://uploadedvideosyoutube.s3.eu-north-1.amazonaws.com/generated/e7f7d437-b341-4d95-a2a7-01c9bfda770e/image_3.png",
"https://uploadedvideosyoutube.s3.eu-north-1.amazonaws.com/generated/4bafc112-2cdc-458d-8c17-6bdca3968e63/image_0.png",
"https://uploadedvideosyoutube.s3.eu-north-1.amazonaws.com/generated/b26c5861-0a44-4e4d-8161-f9993cd534b3/image_1.png",
"https://uploadedvideosyoutube.s3.eu-north-1.amazonaws.com/generated/0a21340a-d134-427b-b99e-eab0c1375996/image_0.png",

"https://uploadedvideosyoutube.s3.eu-north-1.amazonaws.com/generated/4bafc112-2cdc-458d-8c17-6bdca3968e63/image_1.png",
"https://uploadedvideosyoutube.s3.eu-north-1.amazonaws.com/generated/0a21340a-d134-427b-b99e-eab0c1375996/image_3.png",

"https://uploadedvideosyoutube.s3.eu-north-1.amazonaws.com/generated/46b33315-47e8-4783-b1d4-12dab746eabe/image_0.png",
"https://uploadedvideosyoutube.s3.eu-north-1.amazonaws.com/generated/46b33315-47e8-4783-b1d4-12dab746eabe/image_1.png",
"https://uploadedvideosyoutube.s3.eu-north-1.amazonaws.com/generated/b26c5861-0a44-4e4d-8161-f9993cd534b3/image_0.png",
"https://uploadedvideosyoutube.s3.eu-north-1.amazonaws.com/generated/b26c5861-0a44-4e4d-8161-f9993cd534b3/image_3.png",
"https://uploadedvideosyoutube.s3.eu-north-1.amazonaws.com/generated/0a21340a-d134-427b-b99e-eab0c1375996/image_3.png",
"https://uploadedvideosyoutube.s3.eu-north-1.amazonaws.com/generated/b26c5861-0a44-4e4d-8161-f9993cd534b3/image_2.png",
"https://uploadedvideosyoutube.s3.eu-north-1.amazonaws.com/generated/0a21340a-d134-427b-b99e-eab0c1375996/image_0.png",




]
export const endpoints = {
    login:BASE_API + 'auth',
    user_data:BASE_API + 'get_user',
    upload_image:BASE_API + 'upload_image',
    images:BASE_API + 'get_user_images',
    create:BASE_API + 'create',
    photos:BASE_API + 'get_photos',
    photo_status:BASE_API + 'photojob-status',
    billing:BASE_API + 'billing'

}


